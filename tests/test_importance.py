from app.memory.importance import MemoryImportanceScorer


scorer = MemoryImportanceScorer()

examples = [
    "Hello",
    "My favourite language is Python.",
    "Remember I am building HyperGPT.",
    "I have a job interview next week.",
    "Thanks",
    "I am researching multi-agent AI systems using FastAPI and MongoDB."
]

for text in examples:
    result = scorer.score(text)

    print("=" * 50)
    print(text)
    print(result)