from datetime import datetime
from typing import Any, Dict, List, Optional

from backend.app.planner.task import Task


class TaskManager:
    """
    Central task lifecycle manager for HyperGPT.

    Responsibilities:
    - Create tasks
    - Track tasks
    - Manage task states
    - Handle dependencies
    - Handle retries
    - Store execution results
    - Generate execution traces
    """

    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.execution_trace: List[Dict[str, Any]] = []
        self._next_task_id = 1

    # ------------------------------------------------------------------
    # Task Creation
    # ------------------------------------------------------------------

    def create_task(
        self,
        description: str,
        tool: str = "none",
        assigned_agent: Optional[str] = None,
        dependencies: Optional[List[int]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Task:
        """Create and register a new task."""

        task = Task(
            id=self._next_task_id,
            description=description,
            tool=tool,
            assigned_agent=assigned_agent,
            dependencies=dependencies or [],
            metadata=metadata or {},
        )

        self.tasks[task.id] = task
        self._next_task_id += 1

        self._trace(
            "TASK_CREATED",
            task_id=task.id,
            description=task.description,
        )

        return task

    # ------------------------------------------------------------------
    # Task Retrieval
    # ------------------------------------------------------------------

    def get_task(self, task_id: int) -> Optional[Task]:
        """Return a task by ID."""
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Return all registered tasks."""
        return list(self.tasks.values())

    # ------------------------------------------------------------------
    # Lifecycle Management
    # ------------------------------------------------------------------

    def start_task(self, task_id: int) -> Task:
        """Move a task into RUNNING state."""

        task = self._require_task(task_id)

        if not self.dependencies_completed(task):
            raise RuntimeError(
                f"Task {task_id} cannot start because "
                "its dependencies are not completed."
            )

        task.start()

        self._trace(
            "TASK_STARTED",
            task_id=task.id,
            description=task.description,
        )

        return task

    def complete_task(
        self,
        task_id: int,
        result: Any = None,
    ) -> Task:
        """Mark a task as completed."""

        task = self._require_task(task_id)

        task.complete(result)

        self._trace(
            "TASK_COMPLETED",
            task_id=task.id,
            result=result,
        )

        return task

    def fail_task(
        self,
        task_id: int,
        error: str,
    ) -> Task:
        """Mark a task as failed."""

        task = self._require_task(task_id)

        task.fail(error)

        self._trace(
            "TASK_FAILED",
            task_id=task.id,
            error=str(error),
        )

        return task

    def review_task(self, task_id: int) -> Task:
        """Move a task into reviewer state."""

        task = self._require_task(task_id)

        task.review()

        self._trace(
            "TASK_REVIEWING",
            task_id=task.id,
        )

        return task

    # ------------------------------------------------------------------
    # Retry Management
    # ------------------------------------------------------------------

    def retry_task(self, task_id: int) -> bool:
        """
        Retry a failed task.

        Returns True when retry is available.
        """

        task = self._require_task(task_id)

        if not task.retry():
            self._trace(
                "RETRY_LIMIT_REACHED",
                task_id=task.id,
            )
            return False

        self._trace(
            "TASK_RETRY",
            task_id=task.id,
            retry_count=task.retry_count,
        )

        return True

    # ------------------------------------------------------------------
    # Dependency Management
    # ------------------------------------------------------------------

    def dependencies_completed(self, task: Task) -> bool:
        """Check whether all task dependencies are completed."""

        for dependency_id in task.dependencies:
            dependency = self.get_task(dependency_id)

            if dependency is None:
                return False

            if dependency.status != "COMPLETED":
                return False

        return True

    # ------------------------------------------------------------------
    # Status Helpers
    # ------------------------------------------------------------------

    def pending_tasks(self) -> List[Task]:
        """Return tasks waiting for execution."""

        return [
            task
            for task in self.tasks.values()
            if task.status == "PENDING"
        ]

    def failed_tasks(self) -> List[Task]:
        """Return failed tasks."""

        return [
            task
            for task in self.tasks.values()
            if task.status == "FAILED"
        ]

    def completed_tasks(self) -> List[Task]:
        """Return completed tasks."""

        return [
            task
            for task in self.tasks.values()
            if task.status == "COMPLETED"
        ]

    # ------------------------------------------------------------------
    # Execution Trace
    # ------------------------------------------------------------------

    def _trace(
        self,
        event: str,
        task_id: Optional[int] = None,
        **data: Any,
    ) -> None:
        """Record an execution event."""

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "task_id": task_id,
            **data,
        }

        self.execution_trace.append(entry)

    def get_execution_trace(self) -> List[Dict[str, Any]]:
        """Return the complete execution trace."""

        return list(self.execution_trace)

    def get_execution_summary(self) -> Dict[str, Any]:
        """Return a high-level execution summary."""

        tasks = self.get_all_tasks()

        return {
            "total_tasks": len(tasks),
            "pending": len(
                [task for task in tasks if task.status == "PENDING"]
            ),
            "running": len(
                [task for task in tasks if task.status == "RUNNING"]
            ),
            "reviewing": len(
                [task for task in tasks if task.status == "REVIEWING"]
            ),
            "completed": len(
                [task for task in tasks if task.status == "COMPLETED"]
            ),
            "failed": len(
                [task for task in tasks if task.status == "FAILED"]
            ),
            "retrying": len(
                [task for task in tasks if task.status == "RETRY"]
            ),
        }

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Serialize manager state."""

        return {
            "tasks": [
                task.to_dict()
                for task in self.get_all_tasks()
            ],
            "execution_trace": self.get_execution_trace(),
            "summary": self.get_execution_summary(),
        }

    # ------------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------------

    def _require_task(self, task_id: int) -> Task:
        """Retrieve a task or raise a clear error."""

        task = self.get_task(task_id)

        if task is None:
            raise ValueError(
                f"Task with ID {task_id} does not exist."
            )

        return task
