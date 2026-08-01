from app.services.agent_router import AgentRouter
from app.services.response_synthesizer import ResponseSynthesizer


router = AgentRouter()
synthesizer = ResponseSynthesizer()

tasks = [
    "Write Python code to calculate factorial",
    "Plan an AI startup",
    "Write project documentation",
    "Review this documentation",
    "Explain Artificial Intelligence"
]

responses = []

print("=" * 70)
print("HyperGPT Multi-Agent Pipeline Demo")
print("=" * 70)

for task in tasks:
    agent = router.route(task)

    result = agent.execute(task)

    responses.append(result)

    print(f"\nTask   : {task}")
    print(f"Agent  : {agent.name}")
    print(f"Status : {result['status']}")

print("\n" + "=" * 70)

final_response = synthesizer.synthesize(responses)

print("Final Synthesized Response")
print("=" * 70)

print(f"Status      : {final_response['status']}")
print(f"Agents Used : {final_response['agents_used']}")
print(f"Responses   : {len(final_response['responses'])}")

print("=" * 70)