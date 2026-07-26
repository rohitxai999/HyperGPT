from app.agents.base_agent import BaseAgent


class ResearchAgent(BaseAgent):

    def __init__(self):
        super().__init__("Research Agent")

    def can_handle(self, query: str) -> bool:
        keywords = [
            "research",
            "explain",
            "what",
            "why",
            "how",
            "compare",
            "summary",
        ]
        return any(word in query.lower() for word in keywords)

    def run(self, query: str):
        return {
            "agent": self.name,
            "response": f"Researching: {query}",
        }