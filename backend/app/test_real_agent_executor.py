import pytest

from app.core.agent_executor import AgentExecutor
from app.core.planner import TaskPlanner
from app.tools.executor import ToolExecutor


@pytest.mark.asyncio
async def test_real_calculator_tool_execution():

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

    tool_executor = ToolExecutor()

    agent_executor = AgentExecutor(
        tool_executor
    )

    result = await agent_executor.execute_plan(
        plan
    )

    assert result.status == "completed"

    assert result.steps[0].status == "completed"

    assert result.steps[0].result["success"] is True

    assert result.steps[0].result["result"] == 100


@pytest.mark.asyncio
async def test_real_multi_step_execution():

    planner = TaskPlanner()

    plan = planner.create_plan(
        "Multiply 25 by 4 and then add 50"
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

    tool_executor = ToolExecutor()

    agent_executor = AgentExecutor(
        tool_executor
    )

    result = await agent_executor.execute_plan(
        plan
    )

    assert result.status == "completed"

    assert len(result.steps) == 2

    assert result.steps[0].result["result"] == 100

    assert result.steps[1].result["result"] == 150