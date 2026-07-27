class ResearchAgent:
    def process(self, prompt: str) -> str:
        return (
            "📚 Research Agent\n\n"
            f"I received your research request:\n\n{prompt}"
        )