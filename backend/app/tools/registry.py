from typing import Dict
from importlib import import_module
import inspect
import pkgutil

from app.tools.base_tool import BaseTool


class ToolRegistry:
    """
    Registry for all HyperGPT tools.
    """

    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        """Register a tool."""
        self.tools[tool.name] = tool

    def unregister(self, name: str):
        """Remove a tool."""
        self.tools.pop(name, None)

    def get(self, name: str):
        """Get a tool by name."""
        return self.tools.get(name)

    def list_tools(self):
        """Return metadata for all registered tools."""
        return [tool.metadata() for tool in self.tools.values()]

    def auto_register(self):
        """
        Automatically discover and register all tools.
        """

        import app.tools

        for _, module_name, _ in pkgutil.iter_modules(app.tools.__path__):

            if module_name in {
                "__init__",
                "base_tool",
                "registry",
                "selector",
                "logger",
            }:
                continue

            module = import_module(f"app.tools.{module_name}")

            for _, obj in inspect.getmembers(module, inspect.isclass):

                if (
                    issubclass(obj, BaseTool)
                    and obj is not BaseTool
                ):
                    self.register(obj())


# Global registry
registry = ToolRegistry()