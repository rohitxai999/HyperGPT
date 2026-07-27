from groq import Groq

from app.config.settings import GROQ_API_KEY
from app.models.database import SessionLocal
from app.models.chat import Chat

# Multi-Agent Orchestrator
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
            # Multi-Agent Routing
            # -------------------------------------
            agent_response = self.orchestrator.route(message)

            # If Coding, Writing or Planning Agent is selected,
            # return its response immediately.
            if (
                agent_response.startswith("💻")
                or agent_response.startswith("✍️")
                or agent_response.startswith("📅")
            ):
                return agent_response

            # -------------------------------------
            # Create Conversation
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
            # Ask Groq
            # -------------------------------------
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
            return f"Groq Error: {e}"

        finally:
            db.close()