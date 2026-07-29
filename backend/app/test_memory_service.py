from pprint import pprint

from app.services.memory_service import MemoryService

service = MemoryService()

examples = [
    "I'm building HyperGPT.",
    "I love Python.",
    "I have a job interview.",
    "I'm researching RAG systems.",
    "Hello!",
]

for text in examples:
    print("=" * 70)
    pprint(service.analyze(text))