import re
from datetime import datetime


class MemoryImportanceScorer:
    HIGH_PRIORITY_KEYWORDS = [
        "project",
        "goal",
        "career",
        "dream",
        "research",
        "remember",
        "important",
        "deadline",
        "graduation",
        "exam",
        "interview",
        "job",
        "hypergpt",
        "jarvis",
        "forexmind",
        "agentedu",
    ]

    MEDIUM_PRIORITY_KEYWORDS = [
        "python",
        "fastapi",
        "docker",
        "mongodb",
        "study",
        "learning",
        "ai",
        "ml",
        "machine learning",
        "deep learning",
        "university",
        "college",
    ]

    LOW_PRIORITY_KEYWORDS = [
        "hello",
        "hi",
        "thanks",
        "thank you",
        "okay",
        "bye",
    ]

    def score(self, text: str):
        score = 3
        reasons = []

        text_lower = text.lower()

        # Tokenize into whole words
        words = set(re.findall(r"\b[\w-]+\b", text_lower))

        # High priority
        for keyword in self.HIGH_PRIORITY_KEYWORDS:
            if " " in keyword:
                if keyword in text_lower:
                    score += 3
                    reasons.append(f"High keyword: {keyword}")
            elif keyword in words:
                score += 3
                reasons.append(f"High keyword: {keyword}")

        # Medium priority
        for keyword in self.MEDIUM_PRIORITY_KEYWORDS:
            if " " in keyword:
                if keyword in text_lower:
                    score += 2
                    reasons.append(f"Medium keyword: {keyword}")
            elif keyword in words:
                score += 2
                reasons.append(f"Medium keyword: {keyword}")

        # Low priority
        for keyword in self.LOW_PRIORITY_KEYWORDS:
            if " " in keyword:
                if keyword in text_lower:
                    score -= 2
                    reasons.append(f"Low keyword: {keyword}")
            elif keyword in words:
                score -= 2
                reasons.append(f"Low keyword: {keyword}")

        length = len(words)

        if length > 40:
            score += 2
            reasons.append("Long message")
        elif length > 20:
            score += 1
            reasons.append("Medium length")

        score = max(1, min(score, 10))

        return {
            "importance": score,
            "reason": reasons,
            "created_at": datetime.utcnow().isoformat(),
        }