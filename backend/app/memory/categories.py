import re


class MemoryCategoryClassifier:
    """
    Automatically classifies memories into categories.
    """

    CATEGORY_KEYWORDS = {
        "Project": [
            "project",
            "hypergpt",
            "jarvis",
            "forexmind",
            "agentedu",
            "github",
            "repository",
            "application",
        ],
        "Learning": [
            "learn",
            "learning",
            "study",
            "studying",
            "course",
            "tutorial",
            "python",
            "fastapi",
            "mongodb",
            "docker",
            "machine learning",
            "deep learning",
            "ai",
            "ml",
        ],
        "Career": [
            "job",
            "interview",
            "resume",
            "internship",
            "company",
            "salary",
            "career",
            "placement",
        ],
        "Goal": [
            "goal",
            "dream",
            "target",
            "plan",
            "objective",
            "aim",
            "want to",
            "become",
        ],
        "Research": [
            "research",
            "paper",
            "thesis",
            "analysis",
            "rag",
            "llm",
            "agent",
        ],
        "Preference": [
            "favorite",
            "favourite",
            "prefer",
            "like",
            "love",
            "hate",
        ],
        "Personal": [
            "birthday",
            "family",
            "friend",
            "mother",
            "father",
            "brother",
            "sister",
        ],
    }

    def classify(self, text: str):
        text_lower = text.lower()
        words = set(re.findall(r"\b[\w-]+\b", text_lower))

        scores = {}

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            score = 0

            for keyword in keywords:
                if " " in keyword:
                    if keyword in text_lower:
                        score += 1
                elif keyword in words:
                    score += 1

            scores[category] = score

        best_category = max(scores, key=scores.get)

        if scores[best_category] == 0:
            best_category = "Conversation"

        return {
            "category": best_category,
            "confidence": scores.get(best_category, 0),
            "scores": scores,
        }