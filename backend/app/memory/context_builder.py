class ContextBuilder:
    """
    Builds context for the LLM using relevant memories.
    """

    def __init__(self, memory_search):
        self.memory_search = memory_search

    def build_context(self, query: str) -> str:

        memories = self.memory_search.search(query)

        if not memories:
            return "No relevant memories found."

        context = "Relevant Memories:\n\n"

        for memory in memories:
            context += (
                f"- {memory.content} "
                f"(Importance: {memory.importance})\n"
            )

        return context

    def recent_context(self, limit: int = 5) -> str:

        memories = self.memory_search.recent(limit)

        if not memories:
            return "No recent memories."

        context = "Recent Memories:\n\n"

        for memory in memories:
            context += f"- {memory.content}\n"

        return context