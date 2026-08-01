from app.agents.registry import AgentRegistry

registry = AgentRegistry()

print("=" * 60)
print("Available Agents")
print("=" * 60)

for agent in registry.list_agents():
    print(agent)

print("=" * 60)