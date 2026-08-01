from app.agents.registry import AgentRegistry


class AgentRouter:
    """
    Routes user requests to the most appropriate agent.
    """

    def __init__(self):
        self.registry = AgentRegistry()

    def route(self, task: str):
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