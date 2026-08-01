from app.agents.writer_agent import WriterAgent

agent = WriterAgent()

result = agent.execute(
    "Write documentation for a FastAPI project."
)

print("=" * 60)

for key, value in result.items():
    print(f"{key}: {value}")

print("=" * 60)