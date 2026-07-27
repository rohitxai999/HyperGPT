from app.agents.research_agent import ResearchAgent
from app.agents.coding_agent import CodingAgent
from app.agents.writing_agent import WritingAgent
from app.agents.planning_agent import PlanningAgent


class Orchestrator:

    def __init__(self):
        self.research = ResearchAgent()
        self.coding = CodingAgent()
        self.writing = WritingAgent()
        self.planning = PlanningAgent()

    def route(self, prompt: str):

        text = prompt.lower()

        if any(word in text for word in [
            "code",
            "python",
            "java",
            "bug",
            "debug",
            "program",
            "function"
        ]):
            return self.coding.process(prompt)

        elif any(word in text for word in [
            "email",
            "blog",
            "essay",
            "article",
            "write",
            "letter"
        ]):
            return self.writing.process(prompt)

        elif any(word in text for word in [
            "plan",
            "roadmap",
            "schedule",
            "timeline",
            "learning"
        ]):
            return self.planning.process(prompt)

        else:
            return self.research.process(prompt)