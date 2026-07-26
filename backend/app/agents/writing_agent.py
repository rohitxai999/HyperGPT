from app.agents.base_agent import BaseAgent


class WritingAgent(BaseAgent):

    def __init__(self):
        super().__init__("Writing Agent")

    def can_handle(self, query: str) -> bool:
        keywords = [
            "write",
            "essay",
            "email",
            "letter",
            "blog",
            "story",
            "poem",
            "caption",
        ]
        return any(word in query.lower() for word in keywords)

    def run(self, query: str):
        return {
            "agent": self.name,
            "response": f"Writing request received: {query}",
        }