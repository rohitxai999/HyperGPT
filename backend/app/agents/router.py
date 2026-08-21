from app.agents.coding_agent import CodingAgent
from app.agents.writing_agent import WritingAgent
from app.agents.research_agent import ResearchAgent
from app.agents.math_agent import MathAgent
from app.agents.rag_agent import RAGAgent
from app.agents.planner_agent import PlannerAgent


class TaskRouter:

    KEYWORDS = {
        "coding": [
            "code",
            "python",
            "java",
            "javascript",
            "program",
            "programming",
            "function",
            "class",
            "script",
            "debug",
            "bug",
            "algorithm",
            "api",
            "sql",
            "database",
        ],

        "math": [
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
        ],

        "research": [
            "research",
            "explain",
            "what is",
            "what are",
            "why",
            "how does",
            "analyze",
            "analysis",
            "compare",
            "investigate",
            "information",
            "study",
            "report",
        ],

        "writing": [
            "write",
            "rewrite",
            "draft",
            "essay",
            "email",
            "article",
            "story",
            "content",
            "letter",
            "professional",
        ],

        "planning": [
            "plan",
            "planning",
            "roadmap",
            "schedule",
            "timeline",
            "strategy",
            "steps",
            "project plan",
            "learning plan",
            "learning roadmap",
        ],

        "rag": [
            "document",
            "documents",
            "file",
            "files",
            "pdf",
            "uploaded",
            "knowledge base",
            "according to my documents",
            "according to the document",
        ],
    }

    def __init__(self):

        self.agent_map = {
            "coding": CodingAgent(),
            "math": MathAgent(),
            "research": ResearchAgent(),
            "writing": WritingAgent(),
            "planning": PlannerAgent(),
            "rag": RAGAgent(),
        }

    def route(self, query: str):

        query_lower = query.lower()

        scores = {
            agent: 0
            for agent in self.KEYWORDS
        }

        # ---------------------------------
        # Score every capability
        # ---------------------------------

        for agent, keywords in self.KEYWORDS.items():

            for keyword in keywords:

                if keyword in query_lower:
                    scores[agent] += 1

        # ---------------------------------
        # Select all relevant agents
        # ---------------------------------

        selected = [
            agent
            for agent, score in scores.items()
            if score > 0
        ]

        # ---------------------------------
        # Capability fallback
        # ---------------------------------

        if not selected:

            for name, agent in self.agent_map.items():

                try:

                    if agent.can_handle(query):
                        selected.append(name)

                except Exception:
                    continue

        # ---------------------------------
        # Final fallback
        # ---------------------------------

        if not selected:
            selected = ["research"]

        # ---------------------------------
        # Sort by relevance
        # ---------------------------------

        selected.sort(
            key=lambda name: scores[name],
            reverse=True
        )

        return [
            self.agent_map[name]
            for name in selected
        ]
