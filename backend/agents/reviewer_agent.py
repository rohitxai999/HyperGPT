class ReviewerAgent:

    def run(self, task, context=None):

        total_agents = len(context) if context else 0

        return {
            "agent": "Reviewer Agent",
            "status": "completed",
            "result": f"Workflow reviewed for: {task}",
            "agents_reviewed": total_agents,
            "context": context
        }