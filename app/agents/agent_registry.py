from app.agents.research_agent import ResearchAgent
from app.agents.coding_agent import CodingAgent
from app.agents.writing_agent import WritingAgent
from app.agents.planning_agent import PlanningAgent


class AgentRegistry:

    def __init__(self):
        self.agents = {
            "research": ResearchAgent(),
            "coding": CodingAgent(),
            "writing": WritingAgent(),
            "planning": PlanningAgent(),
        }

    def get(self, name: str):
        return self.agents.get(name)

    def names(self):
        return list(self.agents.keys())
