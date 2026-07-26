from app.agents.base_agent import BaseAgent


class MathAgent(BaseAgent):

    def __init__(self):
        super().__init__("Math Agent")

    def can_handle(self, query: str) -> bool:
        keywords = [
            "calculate",
            "solve",
            "equation",
            "math",
            "algebra",
            "integral",
            "derivative",
        ]
        return any(word in query.lower() for word in keywords)

    def run(self, query: str):
        return {
            "agent": self.name,
            "response": f"Solving math problem: {query}",
        }