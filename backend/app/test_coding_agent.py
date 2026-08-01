from app.agents.coding_agent import CodingAgent

agent = CodingAgent()

result = agent.execute(
    "Write Python code to reverse a string."
)

print("=" * 60)

for key, value in result.items():
    print(f"{key}: {value}")

print("=" * 60)