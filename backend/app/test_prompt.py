from chat.prompt import build_prompt

history = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi!"},
]

docs = [
    "Artificial Intelligence is the simulation of human intelligence.",
    "Machine Learning is a subset of AI.",
]

prompt = build_prompt(
    question="What is AI?",
    documents=docs,
    history=history,
)

print(prompt)