from app.database.database import SessionLocal
from app.models.memory import Memory


def main():

    db = SessionLocal()

    try:
        memories = db.query(Memory).all()

        seen = set()
        removed = 0

        for memory in memories:

            key = (
                memory.user_id,
                memory.content
            )

            if key in seen:
                db.delete(memory)
                removed += 1
            else:
                seen.add(key)

        db.commit()

        print(f"Removed duplicates: {removed}")

    finally:
        db.close()


if __name__ == "__main__":
    main()