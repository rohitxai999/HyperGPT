print("Test file started")

from agents.coordinator import Coordinator

workflow = [
    {"type": "research", "task": "Latest AI trends"},
    {"type": "coding", "task": "Python API"},
    {"type": "writing", "task": "Project README"},
    {"type": "math", "task": "25 * 12"},
    {"type": "review", "task": "Final output"},
]

coordinator = Coordinator()

result = coordinator.execute_workflow(workflow)

print("=" * 50)
print("HyperGPT Multi-Agent System")
print("=" * 50)

for item in result["results"]:
    print(item)

print("Test finished")