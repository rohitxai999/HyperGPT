import re

from app.memory.memory_store import MemoryStore


class MemorySearch:
    """
    Keyword-based memory retrieval with stopword filtering.
    """

    STOPWORDS = {
        "i", "me", "my", "mine", "the", "a", "an",
        "is", "are", "am", "was", "were", "be",
        "do", "does", "did", "what", "which", "who",
        "how", "why", "when", "where", "and", "or",
        "to", "of", "for", "in", "on", "with",
        "should", "can", "could", "would", "will",
        "please", "you", "your"
    }

    def __init__(self):
        self.store = MemoryStore()

    def search(self, query: str, limit: int = 5):

        memories = self.store.get_all_memories()

        words = re.findall(
            r"\b[a-zA-Z0-9]+\b",
            query.lower()
        )

        query_words = [
            word
            for word in words
            if word not in self.STOPWORDS
        ]

        if not query_words:
            return []

        results = []

        for memory in memories:

            content = memory.content.lower()

            content_words = set(
                re.findall(
                    r"\b[a-zA-Z0-9]+\b",
                    content
                )
            )

            keyword_matches = sum(
                1
                for word in query_words
                if word in content_words
            )

            if keyword_matches == 0:
                continue

            score = (
                keyword_matches * 5
                + memory.importance
            )

            results.append(
                (score, memory)
            )

        results.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [
            memory
            for score, memory in results[:limit]
        ]

    def recent(self, limit: int = 5):
        return self.store.get_all_memories()[:limit]