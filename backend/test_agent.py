from app.agents.orchestrator import Orchestrator

orchestrator = Orchestrator()

queries = [
    "Write Python FastAPI code",
    "Explain Machine Learning",
    "Write Python code and explain Machine Learning",
    "Summarize this PDF",
]

for query in queries:

    print("=" * 70)
    print("USER:", query)

    result = orchestrator.run(query)

    print("\nFINAL RESPONSE\n")
    print(result["final_response"])