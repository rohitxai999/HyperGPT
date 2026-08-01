from app.agents.research_agent import ResearchAgent
from app.agents.coding_agent import CodingAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.writer_agent import WriterAgent
from app.agents.reviewer_agent import ReviewerAgent


class AgentRegistry:
    """
    Central registry for all HyperGPT agents.
    """

    def __init__(self):
        self.agents = {
            "research": ResearchAgent(),
            "coding": CodingAgent(),
            "planner": PlannerAgent(),
            "writer": WriterAgent(),
            "reviewer": ReviewerAgent(),
        }

    def get(self, name: str):
        return self.agents.get(name)

    def list_agents(self):
        return list(self.agents.keys())