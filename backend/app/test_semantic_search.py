from app.memory.semantic_search import SemanticSearch

search = SemanticSearch()

search.add_memory(1, "HyperGPT Memory Engine")
search.add_memory(2, "ForexMind AI Trading")
search.add_memory(3, "JARVIS Voice Assistant")

results = search.search("HyperGPT AI")

print("Semantic Search Results:\n")

for result in results:
    print(result)