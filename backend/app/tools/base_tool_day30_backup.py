from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseTool(ABC):
    """
    Base class for all HyperGPT tools.
    """

    name: str = "base_tool"
    description: str = "Base tool"
    keywords: List[str] = []

    def prepare_arguments(self, user_input: str) -> Dict[str, Any]:
        """
        Convert the user's request into arguments required by the tool.
        """
        return {}

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool.
        """
        pass

    def metadata(self):
        """
        Return metadata used by the tool-selection engine.
        """

        return {
            "name": self.name,
            "description": self.description,
            "keywords": self.keywords,
        }
