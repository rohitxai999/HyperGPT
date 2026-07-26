from app.agents.base_agent import BaseAgent


class RAGAgent(BaseAgent):

    def __init__(self):
        super().__init__("RAG Agent")

    def can_handle(self, query: str) -> bool:
        keywords = [
            "document",
            "pdf",
            "file",
            "knowledge",
            "rag",
            "retrieve",
        ]
        return any(word in query.lower() for word in keywords)

    def run(self, query: str):
        return {
            "agent": self.name,
            "response": f"Searching knowledge base for: {query}",
        }