import re


class CategoryPredictor:
    """
    Predicts the most appropriate memory category
    from conversation text.
    """

    CATEGORY_KEYWORDS = {
        "Project": [
            "project",
            "github",
            "repository",
            "deploy",
            "application",
            "app",
            "software",
            "system",
            "platform",
        ],
        "Goal": [
            "goal",
            "plan",
            "future",
            "dream",
            "target",
            "mission",
        ],
        "Education": [
            "study",
            "college",
            "assignment",
            "exam",
            "course",
            "learning",
        ],
        "Career": [
            "job",
            "company",
            "internship",
            "career",
            "resume",
            "interview",
        ],
        "Preference": [
            "prefer",
            "favorite",
            "like",
            "better",
            "love",
        ],
        "Task": [
            "todo",
            "task",
            "complete",
            "finish",
            "build",
        ],
        "Idea": [
            "idea",
            "concept",
            "innovation",
            "invent",
            "brainstorm",
        ],
    }

    DEFAULT_CATEGORY = "General"

    @classmethod
    def predict(cls, text: str) -> str:
        text = text.lower()

        scores = {}

        for category, keywords in cls.CATEGORY_KEYWORDS.items():
            score = 0

            for keyword in keywords:
                matches = re.findall(rf"\b{re.escape(keyword)}\b", text)
                score += len(matches)

            scores[category] = score

        best_category = max(scores, key=scores.get)

        if scores[best_category] == 0:
            return cls.DEFAULT_CATEGORY

        return best_category