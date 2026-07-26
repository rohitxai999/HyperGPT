from app.agents.router import TaskRouter


class Orchestrator:
    """
    Coordinates all agents and combines their responses.
    """

    def __init__(self):
        self.router = TaskRouter()

    def run(self, query: str):

        agents = self.router.route(query)

        if not agents:
            return {
                "query": query,
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

        return {
            "query": query,
            "responses": responses,
            "final_response": final_text
        }