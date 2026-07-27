class PlanningAgent:
    def process(self, prompt: str) -> str:
        return (
            "📅 Planning Agent\n\n"
            f"I received your planning request:\n\n{prompt}"
        )