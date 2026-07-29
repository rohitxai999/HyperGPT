from app.agents.router import TaskRouter

from app.memory.memory_store import MemoryStore
from app.memory.semantic_search import SemanticSearch
from app.memory.memory_analyzer import MemoryAnalyzer

from app.services.context_service import ContextService


class Orchestrator:
    """
    Coordinates all agents and combines their responses.
    """

    def __init__(self):

        self.router = TaskRouter()

        # Existing memory system
        self.memory_store = MemoryStore()
        self.semantic = SemanticSearch()
        self.memory_analyzer = MemoryAnalyzer()

        # Day 12 unified context system
        self.context_service = ContextService()


    def run(self, query: str):

        # -----------------------------
        # Retrieve unified context
        # -----------------------------
        context = self.context_service.get_full_context(query)

        related_memories = context["memories"]
        documents = context["documents"]


        agents = self.router.route(query)


        if not agents:
            return {
                "query": query,
                "memories": related_memories,
                "documents": documents,
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
        # Save important memories
        # -----------------------------
        if memory_analysis["importance"] >= 0.5:


            memory = self.memory_store.save_memory(
                content=f"User: {query}\nAssistant: {final_text}",
                user_id="default",
                importance=memory_analysis["importance"]
            )


            # Index memory
            self.semantic.add_memory(
                memory.id,
                memory.content
            )


        return {

            "query": query,

            # Day 12 Context
            "memory_context": related_memories,
            "rag_context": documents,

            # Agent output
            "responses": responses,

            "final_response": final_text
        }