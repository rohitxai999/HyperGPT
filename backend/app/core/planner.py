from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlanStep:
    step_id: int
    description: str
    tool: str
    arguments: dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    result: Any = None


@dataclass
class ExecutionPlan:
    task: str
    steps: list[PlanStep] = field(default_factory=list)
    status: str = "pending"


class TaskPlanner:
    """
    Creates and manages multi-step execution plans.
    """

    def create_plan(self, task: str) -> ExecutionPlan:
        task = task.strip()

        if not task:
            raise ValueError("Task cannot be empty.")

        return ExecutionPlan(
            task=task,
            steps=[]
        )

    def add_step(
        self,
        plan: ExecutionPlan,
        description: str,
        tool: str,
        arguments: dict[str, Any] | None = None,
    ) -> PlanStep:

        step = PlanStep(
            step_id=len(plan.steps) + 1,
            description=description,
            tool=tool,
            arguments=arguments or {},
        )

        plan.steps.append(step)

        return step

    def start(self, plan: ExecutionPlan) -> None:
        plan.status = "running"

    def complete_step(
        self,
        step: PlanStep,
        result: Any,
    ) -> None:

        step.result = result
        step.status = "completed"

    def fail_step(
        self,
        step: PlanStep,
        error: str,
    ) -> None:

        step.result = error
        step.status = "failed"

    def complete_plan(self, plan: ExecutionPlan) -> None:
        plan.status = "completed"

    def fail_plan(self, plan: ExecutionPlan) -> None:
        plan.status = "failed"