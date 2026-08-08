from app.agents.router import TaskRouter

from app.memory.memory_store import MemoryStore
from app.memory.semantic_search import SemanticSearch
from app.memory.memory_analyzer import MemoryAnalyzer

from app.services.context_service import ContextService


class Orchestrator:
    """
    Coordinates HyperGPT agents and provides them
    with memory and RAG context.
    """

    def __init__(self):

        self.router = TaskRouter()

        self.memory_store = MemoryStore()
        self.semantic = SemanticSearch()
        self.memory_analyzer = MemoryAnalyzer()

        self.context_service = ContextService()

    def run(self, query: str):

        # ---------------------------------
        # Retrieve unified context
        # ---------------------------------

        context = self.context_service.get_full_context(query)

        related_memories = context["memories"]
        documents = context["documents"]

        # ---------------------------------
        # Build agent context
        # ---------------------------------

        agent_context = {
            "query": query,
            "memories": related_memories,
            "documents": documents,
        }

        # ---------------------------------
        # Route query
        # ---------------------------------

        agents = self.router.route(query)

        if not agents:

            return {
                "query": query,
                "memory_context": related_memories,
                "rag_context": documents,
                "responses": [],
                "final_response": (
                    "Sorry, I couldn't determine "
                    "which agent should handle this request."
                ),
            }

        responses = []

        # ---------------------------------
        # Execute agents with context
        # ---------------------------------

        for agent in agents:

            try:

                result = agent.run(
                    query,
                    context=agent_context
                )

            except TypeError:

                # Backward compatibility for agents
                # that still accept only query.
                result = agent.run(query)

            responses.append(result)

        # ---------------------------------
        # Synthesize response
        # ---------------------------------

        final_text = "\n".join(
            f"[{r['agent']}] {r['response']}"
            for r in responses
        )

        # ---------------------------------
        # Automatic memory analysis
        # ---------------------------------

        memory_analysis = self.memory_analyzer.analyze(query)

        # ---------------------------------
        # Save important memories
        # ---------------------------------

        if memory_analysis["importance"] >= 0.5:

            memory = self.memory_store.save_memory(
                content=(
                    f"User: {query}\n"
                    f"Assistant: {final_text}"
                ),
                user_id="default",
                importance=memory_analysis["importance"],
            )

            # Index new memory
            self.semantic.add_memory(
                memory.id,
                memory.content,
            )

        return {

            "query": query,

            "memory_context": related_memories,

            "rag_context": documents,

            "agent_context": agent_context,

            "responses": responses,

            "final_response": final_text,
        }