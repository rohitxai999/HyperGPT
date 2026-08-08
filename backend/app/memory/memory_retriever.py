from app.memory.memory_store import MemoryStore
from app.memory.memory_search import MemorySearch
from app.memory.semantic_search import SemanticSearch


class MemoryRetriever:
    """
    Hybrid memory retrieval engine for HyperGPT.

    Combines:
    - keyword search
    - semantic/vector search
    - memory importance
    - retrieval ranking
    - relevance filtering
    """

    MIN_RELEVANCE_SCORE = 0.30

    def __init__(self):
        self.store = MemoryStore()
        self.keyword_search = MemorySearch()
        self.semantic_search = SemanticSearch()

        # Rebuild the semantic index from stored memories.
        self._load_existing_memories()

    def _load_existing_memories(self):
        """
        Load existing database memories into the vector index.
        """

        memories = self.store.get_all_memories()

        for memory in memories:
            try:
                self.semantic_search.add_memory(
                    memory.id,
                    memory.content
                )
            except Exception:
                # Do not allow one invalid memory
                # to break the complete retrieval system.
                continue

    def retrieve(
        self,
        query: str,
        limit: int = 5
    ):
        """
        Retrieve relevant memories using hybrid search.
        """

        if not query or not query.strip():
            return []

        # ---------------------------------
        # Keyword retrieval
        # ---------------------------------

        keyword_memories = self.keyword_search.search(
            query,
            limit=limit * 2
        )

        keyword_map = {
            memory.id: memory
            for memory in keyword_memories
        }

        # ---------------------------------
        # Semantic retrieval
        # ---------------------------------

        semantic_results = self.semantic_search.search(
            query,
            k=limit * 2
        )

        semantic_map = {
            result["memory_id"]: result["distance"]
            for result in semantic_results
        }

        # ---------------------------------
        # Combine candidates
        # ---------------------------------

        candidate_ids = set(keyword_map.keys())
        candidate_ids.update(semantic_map.keys())

        if not candidate_ids:
            return []

        all_memories = self.store.get_all_memories()

        memory_map = {
            memory.id: memory
            for memory in all_memories
        }

        results = []

        for memory_id in candidate_ids:

            memory = memory_map.get(memory_id)

            if memory is None:
                continue

            # ---------------------------------
            # Keyword score
            # ---------------------------------

            keyword_score = 0

            if memory_id in keyword_map:
                keyword_score = 1

            # ---------------------------------
            # Semantic score
            # ---------------------------------

            semantic_score = 0

            if memory_id in semantic_map:

                distance = semantic_map[memory_id]

                # FAISS IndexFlatL2 returns distance.
                # Smaller distance = higher similarity.
                semantic_score = 1 / (1 + distance)

            # ---------------------------------
            # Importance score
            # ---------------------------------

            importance_score = min(
                memory.importance / 10,
                1
            )

            # ---------------------------------
            # Hybrid relevance score
            # ---------------------------------

            final_score = (
                (keyword_score * 0.35)
                + (semantic_score * 0.45)
                + (importance_score * 0.20)
            )

            results.append(
                {
                    "id": memory.id,
                    "content": memory.content,
                    "category": memory.category,
                    "importance": memory.importance,
                    "score": round(final_score, 4),
                    "semantic_score": round(
                        semantic_score,
                        4
                    ),
                    "keyword_score": keyword_score,
                }
            )

        # ---------------------------------
        # Highest relevance first
        # ---------------------------------

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        # ---------------------------------
        # Remove weak/unrelated memories
        # ---------------------------------

        filtered_results = [
            item
            for item in results
            if item["score"] >= self.MIN_RELEVANCE_SCORE
        ]

        return filtered_results[:limit]