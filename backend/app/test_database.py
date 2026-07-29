from app.database.database import SessionLocal
from app.database.memory_repository import MemoryRepository


def main():
    db = SessionLocal()

    try:
        repo = MemoryRepository(db)

        memories = repo.get_all()

        if not memories:
            print("No memories found.")
            return

        for memory in memories:
            print("=" * 60)
            print(f"ID         : {memory.id}")
            print(f"User       : {memory.user_id}")
            print(f"Content    : {memory.content}")
            print(f"Importance : {memory.importance}")
            print(f"Category   : {memory.category}")
            print(f"Created At : {memory.created_at}")

    finally:
        db.close()


if __name__ == "__main__":
    main()