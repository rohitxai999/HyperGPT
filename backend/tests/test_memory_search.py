from app.memory.memory_store import MemoryStore
from app.memory.memory_search import MemorySearch
from app.memory.context_builder import ContextBuilder


def main():
    print("=" * 60)
    print("HyperGPT Day 18 Memory Search Test")
    print("=" * 60)

    store = MemoryStore()

    # Start with a clean database for testing
    store.delete_all()

    # Add test memories
    store.save_memory(
        content="HyperGPT uses a multi-agent architecture.",
        user_id="default",
        importance=5
    )

    store.save_memory(
        content="User prefers FastAPI for backend development.",
        user_id="default",
        importance=4
    )

    store.save_memory(
        content="Complete Day 18 semantic memory search.",
        user_id="default",
        importance=3
    )

    search = MemorySearch()

    print("\nSearching for: FastAPI\n")

    results = search.search("FastAPI")

    for memory in results:
        print(
            f"{memory.content} "
            f"(Importance: {memory.importance})"
        )

    builder = ContextBuilder(search)

    print("\nGenerated Context:\n")
    print(builder.build_context("FastAPI"))

    print("=" * 60)
    print("Day 18 Test Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()