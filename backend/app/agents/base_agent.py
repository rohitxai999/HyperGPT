from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Base class for all HyperGPT agents.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def can_handle(self, query: str) -> bool:
        """
        Return True if this agent can handle the query.
        """
        pass

    @abstractmethod
    def run(self, query: str):
        """
        Execute the agent.
        """
        pass