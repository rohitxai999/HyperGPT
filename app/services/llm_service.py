from groq import Groq
from app.config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


class LLMService:
    def generate_response(self, message: str):

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )

        return response.choices[0].message.content