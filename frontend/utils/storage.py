import json
import os
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_DIR = os.path.join(BASE_DIR, "history")

os.makedirs(HISTORY_DIR, exist_ok=True)


def get_chat_files():
    files = [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]
    return sorted(files)


def create_chat():
    chat_id = str(uuid.uuid4())[:8]
    filename = f"{chat_id}.json"

    with open(os.path.join(HISTORY_DIR, filename), "w", encoding="utf-8") as f:
        json.dump([], f)

    return filename


def load_chat(filename):
    path = os.path.join(HISTORY_DIR, filename)

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_chat(filename, messages):
    path = os.path.join(HISTORY_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)


def delete_chat(filename):
    path = os.path.join(HISTORY_DIR, filename)

    if os.path.exists(path):
        os.remove(path)


def rename_chat(old_name, new_name):
    old_path = os.path.join(HISTORY_DIR, old_name)
    new_path = os.path.join(HISTORY_DIR, f"{new_name}.json")

    if os.path.exists(old_path):
        os.rename(old_path, new_path)

    return f"{new_name}.json"