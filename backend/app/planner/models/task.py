from pydantic import BaseModel, Field
from typing import Dict, Any


class Task(BaseModel):
    id: int
    description: str
    tool: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    status: str = "Pending"
    result: Any = None