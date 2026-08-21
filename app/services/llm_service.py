from groq import Groq

from app.config.settings import GROQ_API_KEY
from app.models.database import SessionLocal
from app.models.chat import Chat

from app.agents.orchestrator import Orchestrator


client = Groq(api_key=GROQ_API_KEY)


class LLMService:

    def __init__(self):
        self.chat_history = {}
        self.orchestrator = Orchestrator()

    def generate_response(
        self,
        message: str,
        chat_id: str = "default",
        model: str = "llama-3.3-70b-versatile"
    ):

        db = SessionLocal()

        try:

            # -------------------------------------
            # Dynamic Multi-Agent Orchestration
            # -------------------------------------

            orchestration = self.orchestrator.route(message)

            agents_used = orchestration["agents_used"]
            agent_responses = orchestration["responses"]

            # -------------------------------------
            # Conversation Initialization
            # -------------------------------------

            if chat_id not in self.chat_history:

                self.chat_history[chat_id] = [
                    {
                        "role": "system",
                        "content": (
                            "You are HyperGPT, an advanced AI assistant. "
                            "Be helpful, accurate, friendly, and professional."
                        )
                    }
                ]

            # -------------------------------------
            # Save User Message
            # -------------------------------------

            self.chat_history[chat_id].append(
                {
                    "role": "user",
                    "content": message
                }
            )

            db.add(
                Chat(
                    chat_id=chat_id,
                    role="user",
                    message=message
                )
            )

            db.commit()

            # -------------------------------------
            # Build Agent Context
            # -------------------------------------

            agent_context = "\n\n".join(
                [
                    f"{name.upper()} AGENT:\n{response}"
                    for name, response
                    in agent_responses.items()
                ]
            )

            # -------------------------------------
            # Ask Groq to Synthesize
            # -------------------------------------

            synthesis_prompt = f"""
You are HyperGPT, a multi-agent AI system.

User request:
{message}

Agents selected:
{", ".join(agents_used)}

Specialist agent results:
{agent_context}

Create one clear, useful, professional answer to the user's
original request.

Do not mention internal implementation details unless useful.
Do not blindly repeat duplicate information.
Use the specialist results as supporting context.
"""

            self.chat_history[chat_id].append(
                {
                    "role": "user",
                    "content": synthesis_prompt
                }
            )

            response = client.chat.completions.create(
                model=model,
                messages=self.chat_history[chat_id],
                temperature=0.7,
                max_tokens=1024
            )

            ai_reply = response.choices[0].message.content

            # -------------------------------------
            # Save Assistant Response
            # -------------------------------------

            self.chat_history[chat_id].append(
                {
                    "role": "assistant",
                    "content": ai_reply
                }
            )

            db.add(
                Chat(
                    chat_id=chat_id,
                    role="assistant",
                    message=ai_reply
                )
            )

            db.commit()

            return ai_reply

        except Exception as e:

            db.rollback()

            return f"HyperGPT Error: {e}"

        finally:

            db.close()
