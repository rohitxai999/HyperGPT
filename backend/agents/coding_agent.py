class CodingAgent:

    def run(self, task, context=None):

        research = ""

        if context:
            research = context.get("Research Agent", "")

        return {
            "agent": "Coding Agent",
            "status": "completed",
            "result": f"Generated code for: {task}",
            "used_research": research
        }