from app.tools.tool_registry import ToolRegistry


class ExecutionEngine:

    def __init__(self):
        self.registry = ToolRegistry()

    def execute(self, tasks):

        results = []

        for task in tasks:

            tool = self.registry.get(task.tool)

            if tool:

                output = tool.execute()

                task.status = "Completed"

                results.append(output)

            else:

                task.status = "Skipped"

                results.append({
                    "tool": task.tool,
                    "result": "Tool not found"
                })

        return results