from app.agents.research_agent import ResearchAgent

agent = ResearchAgent()

result = agent.execute(
    "Explain what Artificial Intelligence is."
)

print("=" * 60)

for key, value in result.items():
    print(f"{key}: {value}")

print("=" * 60)