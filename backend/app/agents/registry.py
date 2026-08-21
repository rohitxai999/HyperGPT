from app.agents.research_agent import ResearchAgent
from app.agents.coding_agent import CodingAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.writer_agent import WriterAgent
from app.agents.writing_agent import WritingAgent
from app.agents.reviewer_agent import ReviewerAgent
from app.agents.math_agent import MathAgent
from app.agents.rag_agent import RAGAgent


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