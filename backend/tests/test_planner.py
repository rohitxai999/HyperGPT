from app.core.planner import TaskPlanner


def test_create_plan():
    planner = TaskPlanner()

    plan = planner.create_plan(
        "Calculate 25 multiplied by 4"
    )

    assert plan.task == "Calculate 25 multiplied by 4"
    assert plan.status == "pending"
    assert len(plan.steps) == 0


def test_add_step():
    planner = TaskPlanner()

    plan = planner.create_plan(
        "Calculate and add numbers"
    )

    step = planner.add_step(
        plan=plan,
        description="Multiply 25 by 4",
        tool="calculator",
        arguments={
            "operation": "multiply",
            "a": 25,
            "b": 4,
        },
    )

    assert step.step_id == 1
    assert step.tool == "calculator"
    assert step.status == "pending"


def test_multiple_steps():
    planner = TaskPlanner()

    plan = planner.create_plan(
        "Calculate multiple operations"
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
        "Add 50",
        "calculator",
        {
            "operation": "add",
            "a": 100,
            "b": 50,
        },
    )

    assert len(plan.steps) == 2
    assert plan.steps[0].step_id == 1
    assert plan.steps[1].step_id == 2


def test_complete_step():
    planner = TaskPlanner()

    plan = planner.create_plan("Test task")

    step = planner.add_step(
        plan,
        "Test operation",
        "calculator",
        {},
    )

    planner.complete_step(step, 150)

    assert step.status == "completed"
    assert step.result == 150


def test_fail_step():
    planner = TaskPlanner()

    plan = planner.create_plan("Test task")

    step = planner.add_step(
        plan,
        "Test operation",
        "calculator",
        {},
    )

    planner.fail_step(step, "Tool execution failed")

    assert step.status == "failed"
    assert step.result == "Tool execution failed"


def test_plan_lifecycle():
    planner = TaskPlanner()

    plan = planner.create_plan("Test lifecycle")

    assert plan.status == "pending"

    planner.start(plan)

    assert plan.status == "running"

    planner.complete_plan(plan)

    assert plan.status == "completed"