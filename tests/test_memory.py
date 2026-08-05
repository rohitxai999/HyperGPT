from memory.memory_manager import MemoryManager
from memory.retrieval import MemoryRetrieval


def main():
    print("=" * 60)
    print("HyperGPT Memory System Test")
    print("=" * 60)

    manager = MemoryManager()

    print("\nAdding memories...")

    manager.remember(
        memory_type="project",
        content="HyperGPT uses a multi-agent architecture.",
        importance=5,
        tags="hypergpt,agents",
    )

    manager.remember(
        memory_type="user",
        content="User prefers FastAPI for backend development.",
        importance=4,
        tags="preference,backend",
    )

    manager.remember(
        memory_type="task",
        content="Complete Day 17 memory system.",
        importance=3,
        tags="day17",
    )

    print("✓ Memories added successfully.")

    print("\nStored Memories")

    memories = manager.recall_all()

    for memory in memories:
        print(
            f"[{memory['id']}] "
            f"{memory['memory_type']} | "
            f"{memory['content']} "
            f"(Importance: {memory['importance']})"
        )

    print("\nSearching for 'HyperGPT'...")

    retrieval = MemoryRetrieval()

    results = retrieval.search("HyperGPT")

    for result in results:
        print(
            f"Found: {result['content']}"
        )

    retrieval.close()
    manager.close()

    print("\n✓ Memory system test completed successfully.")


if __name__ == "__main__":
    main()