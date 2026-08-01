from typing import Any, Dict

from app.agents.base_agent import BaseAgent


class WriterAgent(BaseAgent):
    """
    Writer Agent

    Responsible for:
    - Formatting responses
    - Writing reports
    - Generating documentation
    - Producing Markdown output
    """

    def __init__(self):
        super().__init__(
            name="Writer Agent",
            description="Formats and generates polished text outputs."
        )

    def execute(
        self,
        task: str,
        context: Dict[str, Any] | None = None
    ):
        return {
            "agent": self.name,
            "task": task,
            "document": "",
            "format": "markdown",
            "status": "success"
        }

    def write_document(self, content: str):
        return ""

    def format_markdown(self, text: str):
        return text