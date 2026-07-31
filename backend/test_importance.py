from app.intelligence.memory_importance import MemoryImportanceEngine

print(MemoryImportanceEngine.calculate(mention_count=1))
print(MemoryImportanceEngine.calculate(mention_count=10))
print(MemoryImportanceEngine.calculate(mention_count=50))