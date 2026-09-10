from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Task:
    """
    Core execution task used by HyperGPT's autonomous planner.

    Lifecycle:
        PENDING
        PLANNING
        RUNNING
        REVIEWING
        COMPLETED
        FAILED
        RETRY
    """

    id: int
    description: str
    tool: str = "none"

    status: str = "PENDING"

    assigned_agent: Optional[str] = None

    result: Any = None
    error: Optional[str] = None

    retry_count: int = 0
    max_retries: int = 2

    dependencies: List[int] = field(default_factory=list)

    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    metadata: Dict[str, Any] = field(default_factory=dict)

    def start(self) -> None:
        """Mark the task as running."""
        self.status = "RUNNING"
        self.started_at = datetime.utcnow()
        self.error = None

    def complete(self, result: Any = None) -> None:
        """Mark the task as successfully completed."""
        self.status = "COMPLETED"
        self.result = result
        self.completed_at = datetime.utcnow()

    def fail(self, error: str) -> None:
        """Mark the task as failed."""
        self.status = "FAILED"
        self.error = str(error)
        self.completed_at = datetime.utcnow()

    def retry(self) -> bool:
        """
        Prepare the task for another execution attempt.

        Returns:
            True if retry is available, otherwise False.
        """
        if self.retry_count >= self.max_retries:
            return False

        self.retry_count += 1
        self.status = "RETRY"
        self.error = None
        self.completed_at = None

        return True

    def review(self) -> None:
        """Move the task into the reviewer stage."""
        self.status = "REVIEWING"

    def is_finished(self) -> bool:
        """Return True when the task reached a terminal state."""
        return self.status in {"COMPLETED", "FAILED"}

    def can_retry(self) -> bool:
        """Return whether another execution attempt is available."""
        return self.retry_count < self.max_retries

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the task into a JSON-friendly dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "tool": self.tool,
            "status": self.status,
            "assigned_agent": self.assigned_agent,
            "result": self.result,
            "error": self.error,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "dependencies": self.dependencies,
            "started_at": (
                self.started_at.isoformat()
                if self.started_at
                else None
            ),
            "completed_at": (
                self.completed_at.isoformat()
                if self.completed_at
                else None
            ),
            "metadata": self.metadata,
        }