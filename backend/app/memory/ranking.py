from datetime import datetime


class MemoryRankingEngine:
    """
    Calculates the final ranking score for a memory.

    Formula:
        0.5 * similarity
      + 0.3 * importance
      + 0.2 * recency
    """

    def calculate_score(
        self,
        similarity: float,
        importance: int,
        created_at: datetime,
    ) -> dict:

        # Normalize importance (1–10 -> 0.1–1.0)
        importance_score = importance / 10

        # Days since memory was created
        age_days = (datetime.utcnow() - created_at).days

        # Recency score
        if age_days <= 1:
            recency = 1.0
        elif age_days <= 7:
            recency = 0.8
        elif age_days <= 30:
            recency = 0.6
        elif age_days <= 90:
            recency = 0.4
        else:
            recency = 0.2

        final_score = (
            0.5 * similarity +
            0.3 * importance_score +
            0.2 * recency
        )

        return {
            "similarity": round(similarity, 3),
            "importance": round(importance_score, 3),
            "recency": round(recency, 3),
            "final_score": round(final_score, 3),
        }