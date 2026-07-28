from app.agents.router import TaskRouter

from app.memory.memory_store import MemoryStore
from app.memory.semantic_search import SemanticSearch
from app.memory.memory_analyzer import MemoryAnalyzer


class Orchestrator:
    """
    Coordinates all agents and combines their responses.
    """

    def __init__(self):
        self.router = TaskRouter()

        # Memory components
        self.memory_store = MemoryStore()
        self.semantic = SemanticSearch()
        self.memory_analyzer = MemoryAnalyzer()

    def run(self, query: str):

        # -----------------------------
        # Retrieve related memories
        # -----------------------------
        related_memories = self.semantic.search(query)

        agents = self.router.route(query)

        if not agents:
            return {
                "query": query,
                "related_memories": related_memories,
                "responses": [],
                "final_response": "Sorry, I couldn't determine which agent should handle this request."
            }

        responses = []

        for agent in agents:
            result = agent.run(query)
            responses.append(result)

        final_text = "\n".join(
            f"[{r['agent']}] {r['response']}"
            for r in responses
        )


        # -----------------------------
        # Automatic Memory Analysis
        # -----------------------------
        memory_analysis = self.memory_analyzer.analyze(query)


        # -----------------------------
        # Save only important memories
        # -----------------------------
        if memory_analysis["importance"] >= 0.5:

            memory = self.memory_store.save_memory(
                content=f"User: {query}\nAssistant: {final_text}",
                user_id="default",
                importance=memory_analysis["importance"]
            )

            # -----------------------------
            # Index the new memory
            # -----------------------------
            self.semantic.add_memory(
                memory.id,
                memory.content
            )


        return {
            "query": query,
            "related_memories": related_memories,
            "responses": responses,
            "final_response": final_text
        }