from app.memory.memory_store import MemoryStore


class MemorySearch:

    def __init__(self):
        self.store = MemoryStore()

    def search(self, query: str, limit: int = 5):

        memories = self.store.get_all_memories()

        query = query.lower()

        results = []

        for memory in memories:

            score = 0

            if query in memory.content.lower():
                score += 5

            for word in query.split():
                if word in memory.content.lower():
                    score += 1

            score += memory.importance

            if score > 0:
                results.append((score, memory))

        results.sort(key=lambda x: x[0], reverse=True)

        return [memory for score, memory in results[:limit]]

    def recent(self, limit: int = 5):

        return self.store.get_all_memories()[:limit]