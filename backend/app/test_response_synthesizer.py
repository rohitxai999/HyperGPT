from app.services.response_synthesizer import ResponseSynthesizer

synthesizer = ResponseSynthesizer()

responses = [
    {
        "agent": "Research Agent",
        "facts": ["AI is a branch of computer science."]
    },
    {
        "agent": "Writer Agent",
        "document": "Artificial Intelligence (AI) is a branch of computer science."
    }
]

result = synthesizer.synthesize(responses)

print("=" * 60)

for key, value in result.items():
    print(f"{key}: {value}")

print("=" * 60)