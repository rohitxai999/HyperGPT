from app.tools.registry import ToolRegistry


class Executor:
    """
    Executes tasks created by the Planner.
    """

    def __init__(self):
        self.registry = ToolRegistry()

    def execute(self, tasks):
        completed_tasks = []

        for task in tasks:
            tool = self.registry.get(task.tool)

            if tool is None:
                task.status = "Failed"
                task.result = f"Tool '{task.tool}' not found"
                completed_tasks.append(task)
                continue

            try:
                task.status = "Running"

                if task.parameters:
                    task.result = tool.run(**task.parameters)
                else:
                    task.result = tool.run()

                task.status = "Completed"

            except Exception as e:
                task.status = "Failed"
                task.result = str(e)

            completed_tasks.append(task)

        return completed_tasks