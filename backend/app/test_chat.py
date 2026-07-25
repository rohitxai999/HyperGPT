from app.chat.chat_engine import ChatEngine


def main():
    bot = ChatEngine()

    response = bot.chat("What is Artificial Intelligence?")

    print("\n==============================")
    print("HyperGPT Response")
    print("==============================")
    print(response)


if __name__ == "__main__":
    main()