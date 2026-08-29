from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class PlanStep:
    step_id: int
    description: str
    tool: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    result: Any = None


@dataclass
class Plan:
    task: str
    steps: List[PlanStep] = field(default_factory=list)
    status: str = "pending"

    def __await__(self):
        """
        Allow a Plan to be awaited.

        Supports both:

            result = executor.execute_plan(plan)

        and:

            result = await executor.execute_plan(plan)
        """

        async def _return_self():
            return self

        return _return_self().__await__()


class TaskPlanner:

    def create_plan(self, task: str) -> Plan:
        return Plan(task=task)

    def add_step(
        self,
        plan: Plan,
        description: str,
        tool: str,
        arguments: Dict[str, Any] | None = None,
    ) -> PlanStep:

        step = PlanStep(
            step_id=len(plan.steps) + 1,
            description=description,
            tool=tool,
            parameters=arguments or {},
        )

        plan.steps.append(step)

        return step

    def complete_step(
        self,
        step: PlanStep,
        result: Any = None,
    ) -> PlanStep:

        step.status = "completed"
        step.result = result

        return step

    def fail_step(
        self,
        step: PlanStep,
        error: Any = None,
    ) -> PlanStep:

        step.status = "failed"
        step.result = error

        return step

    def start(
        self,
        plan: Plan,
    ) -> Plan:

        plan.status = "running"

        return plan

    def complete_plan(
        self,
        plan: Plan,
    ) -> Plan:

        plan.status = "completed"

        return plan

    def fail_plan(
        self,
        plan: Plan,
    ) -> Plan:

        plan.status = "failed"

        return plan