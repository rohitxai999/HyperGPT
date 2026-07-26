from app.agents.base_agent import BaseAgent


class CodingAgent(BaseAgent):

    def __init__(self):
        super().__init__("Coding Agent")

    def can_handle(self, query: str) -> bool:
        keywords = [
            "python",
            "code",
            "bug",
            "program",
            "function",
            "api",
            "fastapi",
            "javascript",
        ]
        return any(word in query.lower() for word in keywords)

    def run(self, query: str):
        return {
            "agent": self.name,
            "response": f"Processing coding request: {query}",
        }