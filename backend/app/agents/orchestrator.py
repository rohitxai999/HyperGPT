from typing import Any, Dict, List

from backend.app.agents.router import TaskRouter

from backend.app.memory.memory_store import MemoryStore
from backend.app.memory.semantic_search import SemanticSearch
from backend.app.memory.memory_analyzer import MemoryAnalyzer

from backend.app.services.context_service import ContextService


class Orchestrator:
    """
    Central HyperGPT orchestrator.

    Responsibilities:
    - Retrieve memory and RAG context
    - Route the user query to appropriate agents
    - Execute routed agents
    - Normalize agent responses
    - Store important interactions in memory
    - Return a unified response
    """

    def __init__(self):
        self.router = TaskRouter()

        self.memory_store = MemoryStore()
        self.semantic = SemanticSearch()
        self.memory_analyzer = MemoryAnalyzer()

        self.context_service = ContextService()

    # ==========================================================
    # RESPONSE FORMATTING
    # ==========================================================

    def _format_agent_response(self, result: Any) -> str:
        """
        Convert an agent result into a readable response.
        """

        if not isinstance(result, dict):
            return str(result)

        agent = result.get(
            "agent",
            "Unknown Agent"
        )

        # ------------------------------------------------------
        # Coding Agent
        # ------------------------------------------------------

        if result.get("generated_code"):

            code = result["generated_code"]

            explanation = result.get(
                "explanation",
                ""
            )

            response = (
                f"[{agent}]\n\n"
                f"```python\n"
                f"{str(code).strip()}\n"
                f"```\n"
            )

            if explanation:
                response += (
                    f"\nExplanation:\n"
                    f"{explanation}"
                )

            return response

        # ------------------------------------------------------
        # Planner Agent
        # ------------------------------------------------------

        if result.get("plan"):

            plan = result["plan"]

            response = (
                f"[{agent}]\n\n"
                f"Execution Plan:\n"
            )

            for index, step in enumerate(
                plan,
                start=1
            ):
                response += (
                    f"{index}. {step}\n"
                )

            return response.rstrip()

        # ------------------------------------------------------
        # Autonomous execution result
        # ------------------------------------------------------

        if result.get("results"):

            execution_results = result["results"]

            response = (
                f"[{agent}]\n\n"
                f"Execution Results:\n"
            )

            for item in execution_results:

                task_id = item.get(
                    "task_id",
                    "?"
                )

                status = item.get(
                    "status",
                    "UNKNOWN"
                )

                response += (
                    f"Task {task_id}: "
                    f"{status}\n"
                )

                if item.get("result") is not None:
                    response += (
                        f"Result: "
                        f"{item['result']}\n"
                    )

                if item.get("error"):
                    response += (
                        f"Error: "
                        f"{item['error']}\n"
                    )

            return response.rstrip()

        # ------------------------------------------------------
        # Standard agent response
        # ------------------------------------------------------

        response = result.get(
            "response"
        )

        if response:

            return (
                f"[{agent}]\n\n"
                f"{response}"
            )

        # ------------------------------------------------------
        # Generic task response
        # ------------------------------------------------------

        if result.get("task"):

            return (
                f"[{agent}]\n\n"
                f"Task: {result['task']}"
            )

        # ------------------------------------------------------
        # Generic result
        # ------------------------------------------------------

        if result.get("result") is not None:

            return (
                f"[{agent}]\n\n"
                f"Result: {result['result']}"
            )

        # ------------------------------------------------------
        # Fallback
        # ------------------------------------------------------

        return (
            f"[{agent}]\n\n"
            f"No response generated."
        )

    # ==========================================================
    # AGENT EXECUTION
    # ==========================================================

    async def _execute_agent(
        self,
        agent: Any,
        query: str,
        context: Dict[str, Any],
    ) -> Any:
        """
        Execute an agent while supporting both synchronous
        and asynchronous agent implementations.
        """

        try:

            if hasattr(agent, "run"):

                result = agent.run(
                    query,
                    context=context
                )

            else:

                result = agent.execute(
                    query,
                    context=context
                )

        except TypeError:

            try:

                if hasattr(agent, "run"):
                    result = agent.run(query)
                else:
                    result = agent.execute(query)

            except AttributeError:

                result = agent.execute(query)

        # Handle coroutine results
        if hasattr(result, "__await__"):
            result = await result

        return result

    # ==========================================================
    # MAIN ORCHESTRATION
    # ==========================================================

    async def run(
        self,
        query: str,
    ) -> Dict[str, Any]:
        """
        Execute the complete HyperGPT orchestration pipeline.
        """

        # ------------------------------------------------------
        # Validate query
        # ------------------------------------------------------

        query = str(query).strip()

        if not query:

            return {
                "query": query,
                "memory_context": [],
                "rag_context": [],
                "agent_context": {},
                "responses": [],
                "final_response": (
                    "Please provide a task or question."
                ),
                "status": "failed",
            }

        # ------------------------------------------------------
        # Retrieve unified context
        # ------------------------------------------------------

        context = (
            self.context_service
            .get_full_context(query)
        )

        related_memories = context.get(
            "memories",
            []
        )

        documents = context.get(
            "documents",
            []
        )

        # ------------------------------------------------------
        # Build agent context
        # ------------------------------------------------------

        agent_context = {
            "query": query,
            "memories": related_memories,
            "documents": documents,
        }

        # ------------------------------------------------------
        # Route query
        # ------------------------------------------------------

        agents = self.router.route(query)

        if not agents:

            return {
                "query": query,
                "memory_context": related_memories,
                "rag_context": documents,
                "agent_context": agent_context,
                "responses": [],
                "final_response": (
                    "Sorry, I couldn't determine "
                    "which agent should handle "
                    "this request."
                ),
                "status": "failed",
            }

        # ------------------------------------------------------
        # Execute agents
        # ------------------------------------------------------

        responses: List[Any] = []

        for agent in agents:

            try:

                result = await self._execute_agent(
                    agent,
                    query,
                    agent_context,
                )

                responses.append(result)

            except Exception as exc:

                responses.append(
                    {
                        "agent": getattr(
                            agent,
                            "name",
                            "Unknown Agent"
                        ),
                        "response": (
                            "Agent execution failed: "
                            f"{exc}"
                        ),
                        "status": "failed",
                        "error": str(exc),
                    }
                )

        # ------------------------------------------------------
        # Format responses
        # ------------------------------------------------------

        formatted_responses = [
            self._format_agent_response(
                result
            )
            for result in responses
        ]

        final_text = "\n\n".join(
            formatted_responses
        )

        # ------------------------------------------------------
        # Automatic memory analysis
        # ------------------------------------------------------

        try:

            memory_analysis = (
                self.memory_analyzer
                .analyze(query)
            )

        except Exception:

            memory_analysis = {
                "importance": 0.0
            }

        importance = float(
            memory_analysis.get(
                "importance",
                0.0
            )
        )

        # ------------------------------------------------------
        # Save important memory
        # ------------------------------------------------------

        if importance >= 0.5:

            try:

                memory = (
                    self.memory_store
                    .save_memory(
                        content=(
                            f"User: {query}\n"
                            f"Assistant: {final_text}"
                        ),
                        user_id="default",
                        importance=importance,
                    )
                )

                self.semantic.add_memory(
                    memory.id,
                    memory.content,
                )

            except Exception:
                # Memory failure should not
                # destroy the main response.
                pass

        # ------------------------------------------------------
        # Determine status
        # ------------------------------------------------------

        failed_responses = [
            result
            for result in responses
            if isinstance(result, dict)
            and result.get("status") == "failed"
        ]

        status = (
            "partial"
            if failed_responses
            else "success"
        )

        # ------------------------------------------------------
        # Final unified response
        # ------------------------------------------------------

        return {
            "query": query,
            "memory_context": related_memories,
            "rag_context": documents,
            "agent_context": agent_context,
            "responses": responses,
            "formatted_responses": formatted_responses,
            "final_response": final_text,
            "status": status,
        }