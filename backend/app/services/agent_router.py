from backend.app.agents.registry import AgentRegistry


class AgentRouter:
    """
    Routes user requests to the most appropriate agent.
    """

    def __init__(self, registry=None):
        self.registry = registry or AgentRegistry()

    def route(self, task: str):
        if not isinstance(task, str):
            raise TypeError("task must be a string")

        task_lower = task.lower()

        # -------------------------
        # Coding Agent (Highest Priority)
        # -------------------------
        if any(word in task_lower for word in [
            "code",
            "python",
            "program",
            "debug",
            "bug",
            "fix",
            "function",
            "algorithm",
            "script",
            "class",
            "api"
        ]):
            return self.registry.get("coding")

        # -------------------------
        # Math Agent
        # -------------------------
        # Arithmetic wording must include numbers so ordinary requests such as
        # "add documentation" continue to reach their intended specialist.
        math_concepts = [
            "math",
            "algebra",
            "equation",
            "integral",
            "derivative",
        ]
        arithmetic_words = [
            "add",
            "calculate",
            "solve",
            "multiply",
            "multiplied",
            "times",
            "plus",
            "subtract",
            "minus",
            "divide",
            "divided",
        ]
        has_number = any(character.isdigit() for character in task)

        if any(word in task_lower for word in math_concepts) or (
            has_number
            and any(word in task_lower for word in arithmetic_words)
        ):
            return self.registry.get("math")

        # -------------------------
        # Reviewer Agent
        # -------------------------
        if any(word in task_lower for word in [
            "review",
            "check",
            "verify",
            "improve",
            "inspect",
            "validate",
            "audit"
        ]):
            return self.registry.get("reviewer")

        # -------------------------
        # Writer Agent
        # -------------------------
        if any(word in task_lower for word in [
            "write",
            "documentation",
            "document",
            "report",
            "essay",
            "article",
            "blog",
            "summary"
        ]):
            return self.registry.get("writer")

        # -------------------------
        # Planner Agent
        # -------------------------
        if any(word in task_lower for word in [
            "plan",
            "planning",
            "roadmap",
            "schedule",
            "timeline",
            "strategy",
            "project"
        ]):
            return self.registry.get("planner")

        # -------------------------
        # Default → Research Agent
        # -------------------------
        return self.registry.get("research")
