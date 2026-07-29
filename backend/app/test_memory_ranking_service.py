from datetime import datetime

from app.services.memory_service import MemoryService


service = MemoryService()


result = service.rank_memory(
    similarity=0.92,
    importance=9,
    created_at=datetime.utcnow()
)


print(result)