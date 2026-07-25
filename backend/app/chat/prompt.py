def build_prompt(question: str, documents: list, history: list) -> str:
    """
    Builds the final prompt sent to the LLM.
    """

    history_text = ""

    for message in history:
        role = message["role"].capitalize()
        history_text += f"{role}: {message['content']}\n"

    document_text = "\n\n".join(documents)

    prompt = f"""
You are HyperGPT, an intelligent AI assistant.

Use ONLY the information from the retrieved documents when answering.

========================
Conversation History
========================

{history_text}

========================
Retrieved Documents
========================

{document_text}

========================
User Question
========================

{question}

========================
Answer
========================
"""

    return prompt.strip()