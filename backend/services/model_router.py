from backend.services.groq_service import generate_response as groq_response


def generate_ai_response(message: str, model: str):
    """
    Routes the request to the selected AI model.
    """

    model = model.lower()

    if "llama" in model or "groq" in model:
        return groq_response(message, model)

    elif "gpt" in model:
        return "OpenAI support coming in Day 7."

    elif "ollama" in model:
        return "Ollama support coming in Day 7."

    else:
        # Default to Groq
        return groq_response(message)