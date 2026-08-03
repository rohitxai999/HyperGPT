from app.planner.engine.planner import Planner
from app.planner.engine.executor import Executor


class WorkflowManager:
    """
    Complete HyperGPT execution workflow.
    """

    def __init__(self):
        self.planner = Planner()
        self.executor = Executor()

    def run(self, user_request: str):
        tasks = self.planner.create_plan(user_request)
        results = self.executor.execute(tasks)
        return results