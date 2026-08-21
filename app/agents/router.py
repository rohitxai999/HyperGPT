class DynamicRouter:

    KEYWORDS = {
        "coding": [
            "code",
            "python",
            "java",
            "javascript",
            "bug",
            "debug",
            "program",
            "function",
            "api",
            "database",
            "sql",
            "programming",
        ],
        "writing": [
            "email",
            "blog",
            "essay",
            "article",
            "write",
            "letter",
            "story",
            "content",
            "rewrite",
        ],
        "planning": [
            "plan",
            "roadmap",
            "schedule",
            "timeline",
            "learning",
            "strategy",
            "steps",
            "project plan",
        ],
        "research": [
            "research",
            "analyze",
            "analysis",
            "compare",
            "explain",
            "study",
            "investigate",
            "information",
            "report",
        ],
    }

    def route(self, prompt: str) -> list[str]:

        text = prompt.lower()

        scores = {
            agent: 0
            for agent in self.KEYWORDS
        }

        for agent, keywords in self.KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    scores[agent] += 1

        selected = [
            agent
            for agent, score in scores.items()
            if score > 0
        ]

        # Default agent
        if not selected:
            return ["research"]

        # Sort by relevance
        selected.sort(
            key=lambda agent: scores[agent],
            reverse=True
        )

        return selected
