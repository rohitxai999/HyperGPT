from app.agents.coding_agent import CodingAgent
from app.agents.writing_agent import WritingAgent
from app.agents.research_agent import ResearchAgent
from app.agents.math_agent import MathAgent
from app.agents.rag_agent import RAGAgent


class TaskRouter:

    def __init__(self):

        self.coding_agent = CodingAgent()
        self.writing_agent = WritingAgent()
        self.research_agent = ResearchAgent()
        self.math_agent = MathAgent()
        self.rag_agent = RAGAgent()

        # Specific agents are checked before general agents.
        self.agents = [
            self.coding_agent,
            self.math_agent,
            self.research_agent,
            self.writing_agent,
            self.rag_agent,
        ]

    def route(self, query: str):

        query_lower = query.lower()

        # ---------------------------------
        # Coding priority
        # ---------------------------------

        coding_keywords = [
            "write code",
            "write python",
            "python code",
            "code for",
            "program",
            "programming",
            "function",
            "class",
            "script",
            "debug",
            "bug",
            "algorithm",
            "factorial",
        ]

        if any(
            keyword in query_lower
            for keyword in coding_keywords
        ):
            return [self.coding_agent]

        # ---------------------------------
        # Math priority
        # ---------------------------------

        math_keywords = [
            "calculate",
            "solve",
            "equation",
            "math",
            "algebra",
            "integral",
            "derivative",
            "multiply",
            "add",
            "subtract",
            "divide",
        ]

        if any(
            keyword in query_lower
            for keyword in math_keywords
        ):
            return [self.math_agent]

        # ---------------------------------
        # Research priority
        # ---------------------------------

        research_keywords = [
            "explain",
            "what is",
            "what are",
            "why",
            "how does",
            "research",
            "analyze",
            "analysis",
            "information about",
            "tell me about",
        ]

        if any(
            keyword in query_lower
            for keyword in research_keywords
        ):
            return [self.research_agent]

        # ---------------------------------
        # Writing priority
        # ---------------------------------

        writing_keywords = [
            "write",
            "rewrite",
            "draft",
            "essay",
            "introduction",
            "email",
            "article",
            "story",
            "content",
            "professional",
        ]

        if any(
            keyword in query_lower
            for keyword in writing_keywords
        ):
            return [self.writing_agent]

        # ---------------------------------
        # Capability-based fallback
        # ---------------------------------

        for agent in self.agents:

            try:
                if agent.can_handle(query):
                    return [agent]
            except Exception:
                continue

        # ---------------------------------
        # Final fallback
        # ---------------------------------

        return [self.rag_agent]