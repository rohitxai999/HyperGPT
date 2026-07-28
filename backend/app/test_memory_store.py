from app.database.session import init_database
from app.memory.memory_store import MemoryStore

# Create tables before testing
init_database()

store = MemoryStore()

memory = store.save_memory(
    content="HyperGPT Memory Engine is working!",
    user_id="rohit",
    importance=5
)

print("Saved Memory:")
print(memory.id)
print(memory.content)

print("\nAll Memories:")

for item in store.get_all_memories():
    print(item.id, item.content)