from typing import Dict
from importlib import import_module
import inspect
import pkgutil

from backend.app.tools.base_tool import BaseTool


class ToolRegistry:
    """
    Registry for all HyperGPT tools.

    Responsibilities:
    - Register tools
    - Unregister tools
    - Retrieve tools by name
    - List registered tools
    - Automatically discover tools
    - Ignore backup/internal modules
    """

    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        """Register a tool by its name."""
        self.tools[tool.name] = tool

    def unregister(self, name: str):
        """Remove a tool from the registry."""
        self.tools.pop(name, None)

    def get(self, name: str):
        """Get a registered tool by name."""
        return self.tools.get(name)

    def list_tools(self):
        """Return metadata for all registered tools."""
        return [tool.metadata() for tool in self.tools.values()]

    def auto_register(self):
        """
        Automatically discover and register all valid HyperGPT tools.

        Backup files, private modules, registry internals, and imported
        BaseTool classes are ignored.
        """

        import backend.app.tools

        excluded_modules = {
            "__init__",
            "base_tool",
            "registry",
            "selector",
            "logger",
        }

        for _, module_name, _ in pkgutil.iter_modules(
            backend.app.tools.__path__
        ):
            # Ignore internal modules
            if module_name in excluded_modules:
                continue

            # Ignore private modules
            if module_name.startswith("_"):
                continue

            # Ignore Day backup files
            if "_day" in module_name and "backup" in module_name:
                continue

            # Import the discovered tool module
            module = import_module(
                f"backend.app.tools.{module_name}"
            )

            # Find BaseTool subclasses defined by this module
            for _, obj in inspect.getmembers(
                module,
                inspect.isclass
            ):
                if (
                    issubclass(obj, BaseTool)
                    and obj is not BaseTool
                    and obj.__module__ == module.__name__
                ):
                    self.register(obj())


# Global registry instance
registry = ToolRegistry()