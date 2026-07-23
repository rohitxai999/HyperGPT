import os
from groq import Groq

# Create Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_response(message, model="llama-3.3-70b-versatile"):
    """
    Generate AI response using Groq.
    """

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are HyperGPT, an advanced AI assistant. "
                        "Be accurate, helpful, and concise."
                    ),
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Groq Error: {str(e)}"