from app.agents.reviewer_agent import ReviewerAgent

agent = ReviewerAgent()

result = agent.execute(
    "Review this generated report."
)

print("=" * 60)

for key, value in result.items():
    print(f"{key}: {value}")

print("=" * 60)