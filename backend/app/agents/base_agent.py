from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """
    Base class for every HyperGPT agent.
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, task: str, context: Dict[str, Any] | None = None):
        """Execute the assigned task."""
        pass

    def info(self):
        return {
            "name": self.name,
            "description": self.description,
        }