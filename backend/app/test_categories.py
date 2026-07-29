from app.memory.categories import MemoryCategoryClassifier

classifier = MemoryCategoryClassifier()

examples = [
    "I'm building HyperGPT.",
    "I love Python.",
    "I have a job interview next week.",
    "My goal is to become an AI Engineer.",
    "I'm researching RAG systems.",
    "Hello, how are you?",
    "My birthday is tomorrow.",
]

for text in examples:
    result = classifier.classify(text)

    print("=" * 60)
    print(text)
    print(result)