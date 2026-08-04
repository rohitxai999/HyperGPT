class MathAgent:

    def run(self, task, context=None):

        return {
            "agent": "Math Agent",
            "status": "completed",
            "result": f"Calculated solution for: {task}",
            "context": context
        }