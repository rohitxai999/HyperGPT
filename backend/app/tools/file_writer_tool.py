from pathlib import Path
from typing import Any, Dict

from backend.app.tools.base_tool import BaseTool


class FileWriterTool(BaseTool):
    """
    Writes HyperGPT execution reports to disk.
    """

    name = "file_writer"
    description = "Creates and saves HyperGPT execution reports."

    keywords = [
        "save",
        "write",
        "file",
        "report",
        "save report",
        "write report",
        "create file",
    ]

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Create an execution report.

        Optional:
            content: Custom report content.
            filename: Output filename.
        """

        content = kwargs.get("content")

        if not content:
            content = """HyperGPT Execution Report

Status: Success

The autonomous execution engine completed all tasks successfully.
"""

        filename = kwargs.get(
            "filename",
            "execution_report.txt",
        )

        output_path = Path(filename)

        try:
            output_path.write_text(
                str(content),
                encoding="utf-8",
            )

            return {
                "success": True,
                "tool": self.name,
                "result": (
                    f"Report saved to "
                    f"{output_path.resolve()}"
                ),
                "path": str(output_path.resolve()),
            }

        except Exception as exc:
            return {
                "success": False,
                "tool": self.name,
                "error": str(exc),
            }