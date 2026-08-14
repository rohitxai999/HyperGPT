from app.memory.memory_store import MemoryStore


def test_memory_store():
    memory_store = MemoryStore()

    memory = memory_store.save_memory(
        content="User: Hello\nAssistant: Hi! How can I help you?",
        user_id="test_user",
        importance=0.8,
    )

    assert memory is not None
    assert memory.content == (
        "User: Hello\nAssistant: Hi! How can I help you?"
    )

    second_memory = memory_store.save_memory(
        content="User: Explain AI.",
        user_id="test_user",
        importance=0.8,
    )

    assert second_memory is not None
    assert second_memory.content == "User: Explain AI."