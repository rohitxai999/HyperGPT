class WritingAgent:

    def run(self, task, context=None):

        return {
            "agent": "Writing Agent",
            "status": "completed",
            "result": f"Documentation created for: {task}",
            "context": context
        }