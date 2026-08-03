from app.planner.models.task import Task


class Planner:
    """
    Converts a user request into executable tasks.
    """

    def create_plan(self, user_request: str):
        request = user_request.lower()

        tasks = []
        task_id = 1

        if "calculate" in request:
            tasks.append(
                Task(
                    id=task_id,
                    description="Perform calculation",
                    tool="calculator",
                    parameters={
                        "expression": "20*5+8"
                    }
                )
            )
            task_id += 1

        if "time" in request:
            tasks.append(
                Task(
                    id=task_id,
                    description="Get current time",
                    tool="time"
                )
            )

        return tasks