from chat.memory import ConversationMemory

memory = ConversationMemory()

memory.add_user_message("Hello")
memory.add_ai_message("Hi! How can I help you?")

memory.add_user_message("Explain AI.")

for msg in memory.get_history():
    print(msg)