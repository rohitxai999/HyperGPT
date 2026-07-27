class WritingAgent:
    def process(self, prompt: str) -> str:
        return (
            "✍️ Writing Agent\n\n"
            f"I received your writing request:\n\n{prompt}"
        )