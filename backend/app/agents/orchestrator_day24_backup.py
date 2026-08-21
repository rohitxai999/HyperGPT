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

    def _format_agent_response(self, result: dict) -> str:
        """
        Convert different agent response formats into
        one clean final response.
        """

        agent = result.get(
            "agent",
            "Unknown Agent"
        )

        # ---------------------------------
        # Coding Agent
        # ---------------------------------

        if result.get("generated_code"):

            code = result["generated_code"]

            explanation = result.get(
                "explanation",
                ""
            )

            response = (
                f"[{agent}]\n\n"
                f"```python\n"
                f"{code.strip()}\n"
                f"```\n"
            )

            if explanation:
                response += (
                    f"\nExplanation:\n"
                    f"{explanation}"
                )

            return response

        # ---------------------------------
        # Normal agents
        # ---------------------------------

        response = result.get(
            "response"
        )

        if response:
            return (
                f"[{agent}] "
                f"{response}"
            )

        # ---------------------------------
        # Fallback
        # ---------------------------------

        return (
            f"[{agent}] "
            f"No response generated."
        )

    def run(self, query: str):

        # ---------------------------------
        # Retrieve unified context
        # ---------------------------------

        context = self.context_service.get_full_context(
            query
        )

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

        agents = self.router.route(
            query
        )

        if not agents:

            return {
                "query": query,
                "memory_context": related_memories,
                "rag_context": documents,
                "responses": [],
                "final_response": (
                    "Sorry, I couldn't determine "
                    "which agent should handle "
                    "this request."
                ),
            }

        responses = []

        # ---------------------------------
        # Execute agents
        # ---------------------------------

        for agent in agents:

            try:

                result = agent.run(
                    query,
                    context=agent_context
                )

            except AttributeError:

                # Some agents implement execute()
                # instead of run().

                result = agent.execute(
                    query,
                    context=agent_context
                )

            except TypeError:

                # Backward compatibility for agents
                # that only accept query.

                try:
                    result = agent.run(
                        query
                    )
                except AttributeError:
                    result = agent.execute(
                        query
                    )

            responses.append(
                result
            )

        # ---------------------------------
        # Build final response
        # ---------------------------------

        formatted_responses = [
            self._format_agent_response(
                result
            )
            for result in responses
        ]

        final_text = "\n\n".join(
            formatted_responses
        )

        # ---------------------------------
        # Automatic memory analysis
        # ---------------------------------

        memory_analysis = (
            self.memory_analyzer.analyze(
                query
            )
        )

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
                importance=(
                    memory_analysis["importance"]
                ),
            )

            self.semantic.add_memory(
                memory.id,
                memory.content,
            )

        # ---------------------------------
        # Final result
        # ---------------------------------

        return {

            "query": query,

            "memory_context": (
                related_memories
            ),

            "rag_context": (
                documents
            ),

            "agent_context": (
                agent_context
            ),

            "responses": responses,

            "final_response": (
                final_text
            ),
        }