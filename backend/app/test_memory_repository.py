from app.database.database import SessionLocal
from app.database.memory_repository import MemoryRepository


def main():

    db = SessionLocal()

    try:

        repo = MemoryRepository(db)

        print("=" * 60)
        print("ALL MEMORIES")

        memories = repo.get_all()

        for memory in memories:
            print(
                {
                    "id": memory.id,
                    "content": memory.content,
                    "importance": memory.importance,
                    "category": memory.category,
                }
            )


        print("=" * 60)
        print("RECENT MEMORIES")

        recent = repo.get_recent_memories()

        for memory in recent:
            print(
                {
                    "content": memory.content,
                    "category": memory.category,
                }
            )


        print("=" * 60)
        print("SEARCH: HyperGPT")

        results = repo.search_memories("HyperGPT")

        for memory in results:
            print(
                {
                    "content": memory.content,
                    "importance": memory.importance,
                }
            )


    finally:
        db.close()


if __name__ == "__main__":
    main()