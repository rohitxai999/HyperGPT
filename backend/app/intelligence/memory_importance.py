import math
from datetime import datetime


class MemoryImportanceEngine:
    """
    Calculates a dynamic importance score for memories.
    """

    BASE_IMPORTANCE = 5
    MAX_IMPORTANCE = 10
    MIN_IMPORTANCE = 1

    @classmethod
    def calculate(
        cls,
        mention_count: int = 1,
        days_old: int = 0,
        user_rating: int | None = None,
    ) -> int:
        """
        Returns an importance score between 1 and 10.
        """

        score = cls.BASE_IMPORTANCE

        # Frequently discussed topics become more important
        score += math.log(max(mention_count, 1), 2)

        # Older memories slowly lose importance
        score -= days_old / 30

        # Explicit user rating overrides slightly
        if user_rating is not None:
            score += (user_rating - 5) * 0.5

        score = max(cls.MIN_IMPORTANCE, score)
        score = min(cls.MAX_IMPORTANCE, score)

        return round(score)

    @classmethod
    def update_after_access(cls, current_importance: int):
        """
        Increase importance when a memory is reused.
        """

        return min(cls.MAX_IMPORTANCE, current_importance + 1)

    @classmethod
    def decay(cls, current_importance: int):
        """
        Slowly decay unused memories.
        """

        return max(cls.MIN_IMPORTANCE, current_importance - 1)