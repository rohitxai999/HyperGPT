from dataclasses import dataclass


@dataclass
class Memory:
    id: int | None = None
    memory_type: str = ""
    content: str = ""
    importance: int = 1
    tags: str = ""