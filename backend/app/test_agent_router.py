from app.services.agent_router import AgentRouter

router = AgentRouter()

tasks = [
    "Write Python code to reverse a string",
    "Plan an AI startup",
    "Write project documentation",
    "Review this report",
    "Explain Machine Learning"
]

print("=" * 60)

for task in tasks:
    agent = router.route(task)
    print(f"Task : {task}")
    print(f"Agent: {agent.name}")
    print("-" * 60)