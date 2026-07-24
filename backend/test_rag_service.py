from pathlib import Path

from app.services.rag_service import (
    process_document,
    ask_document,
)

UPLOADS = Path("uploads")

pdf = list(UPLOADS.glob("*.pdf"))[0]

print(process_document(str(pdf)))

print()

response = ask_document(
    "What is this document about?"
)

print(response)