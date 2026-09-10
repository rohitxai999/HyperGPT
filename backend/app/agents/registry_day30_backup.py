from backend.app.agents.research_agent import ResearchAgent
from backend.app.agents.coding_agent import CodingAgent
from backend.app.agents.planner_agent import PlannerAgent
from backend.app.agents.writer_agent import WriterAgent
from backend.app.agents.writing_agent import WritingAgent
from backend.app.agents.reviewer_agent import ReviewerAgent
from backend.app.agents.math_agent import MathAgent
from backend.app.agents.rag_agent import RAGAgent


class AgentRegistry:
    """
    Central registry for all HyperGPT agents.

    The registry provides a single source of truth for
    agent discovery and retrieval.
    """

    def __init__(self):
        self.agents = {
            "research": ResearchAgent(),
            "coding": CodingAgent(),
            "planner": PlannerAgent(),
            "writer": WriterAgent(),
            "writing": WritingAgent(),
            "reviewer": ReviewerAgent(),
            "math": MathAgent(),
            "rag": RAGAgent(),
        }

    def get(self, name: str):
        """
        Retrieve an agent by its registered name.
        """
        return self.agents.get(name)

    def list_agents(self):
        """
        Return all registered agent names.
        """
        return list(self.agents.keys())

    def has_agent(self, name: str) -> bool:
        """
        Check whether an agent exists in the registry.
        """
        return name in self.agents

    def get_agent_info(self):
        """
        Return metadata for all registered agents.
        """
        return {
            name: agent.info()
            for name, agent in self.agents.items()
        }
