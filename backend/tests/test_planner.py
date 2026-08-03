from app.execution.workflow import WorkflowManager

workflow = WorkflowManager()

results = workflow.run(
    "Calculate something and tell me the time"
)

print("\n===== HyperGPT Workflow Report =====\n")

for task in results:
    print(task.model_dump())