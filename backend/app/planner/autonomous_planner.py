from app.planner.task import Task


class AutonomousPlanner:

    def create_plan(self, prompt: str):

        tasks = []

        prompt = prompt.lower()

        if "calculate" in prompt:
            tasks.append(
                Task(
                    id=1,
                    description="Perform calculation",
                    tool="calculator"
                )
            )

        if "time" in prompt:
            tasks.append(
                Task(
                    id=len(tasks) + 1,
                    description="Get current time",
                    tool="time"
                )
            )

        if "save" in prompt:
            tasks.append(
                Task(
                    id=len(tasks) + 1,
                    description="Save report",
                    tool="file_writer"
                )
            )

        if not tasks:
            tasks.append(
                Task(
                    id=1,
                    description="General reasoning",
                    tool="none"
                )
            )

        return tasks