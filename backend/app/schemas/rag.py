from pydantic import BaseModel


class AskDocumentRequest(BaseModel):
    question: str


class AskDocumentResponse(BaseModel):
    question: str
    answer: str
    sources: int