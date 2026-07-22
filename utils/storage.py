import json
import os
import uuid

HISTORY_DIR = "history"

os.makedirs(HISTORY_DIR, exist_ok=True)


def get_chat_files():
    files = [
        f for f in os.listdir(HISTORY_DIR)
        if f.endswith(".json")
    ]
    return sorted(files)


def create_chat():
    chat_id = str(uuid.uuid4())[:8]
    filename = f"{chat_id}.json"

    with open(os.path.join(HISTORY_DIR, filename), "w") as f:
        json.dump([], f)

    return filename


def load_chat(filename):
    path = os.path.join(HISTORY_DIR, filename)

    if not os.path.exists(path):
        return []

    with open(path, "r") as f:
        return json.load(f)


def save_chat(filename, messages):
    path = os.path.join(HISTORY_DIR, filename)

    with open(path, "w") as f:
        json.dump(messages, f, indent=4)


def delete_chat(filename):
    path = os.path.join(HISTORY_DIR, filename)

    if os.path.exists(path):
        os.remove(path)