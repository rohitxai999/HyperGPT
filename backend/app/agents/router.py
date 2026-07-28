from app.agents.coding_agent import CodingAgent
from app.agents.writing_agent import WritingAgent
from app.agents.research_agent import ResearchAgent
from app.agents.math_agent import MathAgent
from app.agents.rag_agent import RAGAgent


class TaskRouter:

    def __init__(self):
        self.agents = [
            CodingAgent(),
            WritingAgent(),
            ResearchAgent(),
            MathAgent(),
            RAGAgent(),
        ]

    def route(self, query: str):

        matched = []

        for agent in self.agents:
            try:
                if agent.can_handle(query):
                    matched.append(agent)
            except Exception:
                pass

        # -----------------------------
        # Fallback
        # -----------------------------
        if not matched:
            matched.append(self.agents[-1])   # Default to RAGAgent

        return matched