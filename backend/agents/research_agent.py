class ResearchAgent:

    def run(self, task, context=None):
        return {
            "agent": "Research Agent",
            "status": "completed",
            "result": f"Research completed for: {task}"
        }
