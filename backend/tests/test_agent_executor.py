from app.core.agent_executor import AgentExecutor
from app.core.planner import TaskPlanner


class MockToolExecutor:

    def execute(self, tool, arguments):
        if tool != "calculator":
            raise ValueError(f"Unknown tool: {tool}")

        operation = arguments["operation"]
        a = arguments["a"]
        b = arguments["b"]

        if operation == "add":
            return a + b

        if operation == "multiply":
            return a * b

        raise ValueError(
            f"Unsupported operation: {operation}"
        )


def test_execute_single_step():
    planner = TaskPlanner()

    plan = planner.create_plan(
        "Multiply 25 by 4"
    )

    planner.add_step(
        plan,
        "Multiply 25 by 4",
        "calculator",
        {
            "operation": "multiply",
            "a": 25,
            "b": 4,
        },
    )

    executor = AgentExecutor(
        MockToolExecutor()
    )

    result = executor.execute_plan(plan)

    assert result.status == "completed"
    assert result.steps[0].status == "completed"
    assert result.steps[0].result == 100


def test_execute_multiple_steps():
    planner = TaskPlanner()

    plan = planner.create_plan(
        "Multiply 25 by 4 and add 50"
    )

    planner.add_step(
        plan,
        "Multiply 25 by 4",
        "calculator",
        {
            "operation": "multiply",
            "a": 25,
            "b": 4,
        },
    )

    planner.add_step(
        plan,
        "Add 50 to 100",
        "calculator",
        {
            "operation": "add",
            "a": 100,
            "b": 50,
        },
    )

    executor = AgentExecutor(
        MockToolExecutor()
    )

    result = executor.execute_plan(plan)

    assert result.status == "completed"

    assert result.steps[0].status == "completed"
    assert result.steps[0].result == 100

    assert result.steps[1].status == "completed"
    assert result.steps[1].result == 150


def test_failed_step_fails_plan():
    planner = TaskPlanner()

    plan = planner.create_plan(
        "Execute invalid operation"
    )

    planner.add_step(
        plan,
        "Invalid calculator operation",
        "calculator",
        {
            "operation": "divide",
            "a": 10,
            "b": 0,
        },
    )

    executor = AgentExecutor(
        MockToolExecutor()
    )

    result = executor.execute_plan(plan)

    assert result.status == "failed"
    assert result.steps[0].status == "failed"