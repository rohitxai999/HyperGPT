from app.intelligence.category_predictor import CategoryPredictor

texts = [
    "Continue HyperGPT development",
    "I want to become an AI engineer",
    "My exam is tomorrow",
    "I prefer FastAPI",
    "Finish the dashboard",
]

for text in texts:
    print(text)
    print("Category:", CategoryPredictor.predict(text))
    print("-" * 40)