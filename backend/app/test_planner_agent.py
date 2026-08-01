from app.agents.planner_agent import PlannerAgent

agent = PlannerAgent()

result = agent.execute(
    "Build an AI-powered chatbot."
)

print("=" * 60)

for key, value in result.items():
    print(f"{key}: {value}")

print("=" * 60)