from app.agents.orchestrator import Orchestrator

orchestrator = Orchestrator()

prompts = [
    "Explain Machine Learning",
    "Write a resignation email",
    "Create a 6 month AI roadmap",
    "Debug this Python code"
]

for prompt in prompts:
    print("=" * 60)
    print("USER:", prompt)
    print()
    print(orchestrator.route(prompt))
    print()