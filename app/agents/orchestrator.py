from app.agents.agent_registry import AgentRegistry
from app.agents.router import DynamicRouter


class Orchestrator:

    def __init__(self):
        self.registry = AgentRegistry()
        self.router = DynamicRouter()

    def route(self, prompt: str):

        agents_used = self.router.route(prompt)

        responses = {}

        for agent_name in agents_used:

            agent = self.registry.get(agent_name)

            if agent is None:
                continue

            try:
                responses[agent_name] = agent.process(prompt)

            except Exception as exc:
                responses[agent_name] = (
                    f"Agent execution error: {exc}"
                )

        final_response = self.synthesize(
            prompt,
            agents_used,
            responses
        )

        return {
            "agents_used": agents_used,
            "responses": responses,
            "final_response": final_response,
        }

    def synthesize(
        self,
        prompt: str,
        agents_used: list[str],
        responses: dict
    ) -> str:

        if not responses:
            return "I was unable to execute an appropriate agent."

        # For now, combine specialist responses.
        # LLM-based synthesis will be added after the
        # orchestration pipeline is verified.

        parts = []

        for agent_name, response in responses.items():

            parts.append(
                f"[{agent_name.upper()} AGENT]\n{response}"
            )

        return "\n\n".join(parts)
