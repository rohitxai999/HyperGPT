from datetime import datetime, timedelta

from app.memory.ranking import MemoryRankingEngine

engine = MemoryRankingEngine()

examples = [
    {
        "similarity": 0.95,
        "importance": 9,
        "created_at": datetime.utcnow() - timedelta(hours=2),
    },
    {
        "similarity": 0.80,
        "importance": 7,
        "created_at": datetime.utcnow() - timedelta(days=5),
    },
    {
        "similarity": 0.60,
        "importance": 10,
        "created_at": datetime.utcnow() - timedelta(days=45),
    },
]

for i, memory in enumerate(examples, start=1):
    print("=" * 60)
    print(f"Memory {i}")

    result = engine.calculate_score(
        similarity=memory["similarity"],
        importance=memory["importance"],
        created_at=memory["created_at"],
    )

    print(result)