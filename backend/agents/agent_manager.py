from agents.research_agent import ResearchAgent
from agents.coding_agent import CodingAgent
from agents.writing_agent import WritingAgent
from agents.math_agent import MathAgent
from agents.reviewer_agent import ReviewerAgent


class AgentManager:
    def __init__(self):
        self.agents = {
            "research": ResearchAgent(),
            "coding": CodingAgent(),
            "writing": WritingAgent(),
            "math": MathAgent(),
            "review": ReviewerAgent(),
        }

    def get_agent(self, task_type):
        return self.agents.get(task_type)

    def execute(self, task_type, task, context=None):
        agent = self.get_agent(task_type)

        if not agent:
            return {
                "status": "error",
                "message": f"No agent found for '{task_type}'"
            }

        return agent.run(task, context)