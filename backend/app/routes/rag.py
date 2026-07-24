from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.schemas.rag import (
    AskDocumentRequest,
    AskDocumentResponse,
)

from app.services.rag_service import (
    process_document,
    ask_document,
)

from app.rag.retriever import retrieve_documents


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)


# -------------------------
# Query Request Model
# -------------------------

class QueryRequest(BaseModel):
    question: str



# -------------------------
# Upload Document
# -------------------------

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    file_path = UPLOADS_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    result = process_document(
        str(file_path)
    )

    return {
        "filename": file.filename,
        **result,
    }



# -------------------------
# Ask Document (LLM)
# -------------------------

@router.post(
    "/ask",
    response_model=AskDocumentResponse,
)
async def ask_document_api(
    request: AskDocumentRequest,
):

    try:

        result = ask_document(
            request.question
        )

        return result


    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )



# -------------------------
# RAG Retrieval Query
# -------------------------

@router.post("/query")
async def rag_query(
    request: QueryRequest
):

    try:

        documents = retrieve_documents(
            request.question
        )


        return {

            "question": request.question,

            "results": documents

        }


    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )