from fastapi import APIRouter, UploadFile

router = APIRouter(
    prefix="/embeddings",
    tags=["embeddings"],
)

@router.post("/documents")
async def embed_document(file: UploadFile):
    return {"filename": file.filename}