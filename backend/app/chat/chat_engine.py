import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from app.chat.memory import ConversationMemory
from app.chat.prompt import build_prompt
from app.rag.retriever import retrieve_documents

load_dotenv()


class ChatEngine:

    def __init__(self):

        self.memory = ConversationMemory()

        self.llm = ChatGroq(
            model="openai/gpt-oss-20b",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0,
        )

    def chat(self, question: str):

        docs = retrieve_documents(question)

        document_text = [
            str(doc)
            for doc in docs
        ]

        prompt = build_prompt(
            question=question,
            documents=document_text,
            history=self.memory.get_history(),
        )

        response = self.llm.invoke(prompt)

        answer = response.content

        self.memory.add_user_message(question)
        self.memory.add_ai_message(answer)

        return answer
