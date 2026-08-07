from fastapi import APIRouter
from pydantic import BaseModel

from app.tools.registry import registry
from app.tools.executor import ToolExecutor
from app.tools.logger import logger

router = APIRouter(
    prefix="/tools",
    tags=["Tools"]
)

executor = ToolExecutor()


class ToolRequest(BaseModel):
    user_input: str


@router.get("/")
def list_tools():
    registry.auto_register()
    return registry.list_tools()


@router.post("/run")
async def run_tool(request: ToolRequest):
    return await executor.execute(request.user_input)


@router.get("/history")
def tool_history():
    return logger.get_history()