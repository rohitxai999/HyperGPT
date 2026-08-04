from agents.agent_manager import AgentManager


class Coordinator:

    def __init__(self):
        self.manager = AgentManager()

    def execute_workflow(self, workflow):

        context = {}
        results = []

        for step in workflow:

            result = self.manager.execute(
                step["type"],
                step["task"],
                context
            )

            # Store each agent's output for later agents
            context[result["agent"]] = result["result"]

            results.append(result)

        return {
            "status": "completed",
            "context": context,
            "results": results
        }