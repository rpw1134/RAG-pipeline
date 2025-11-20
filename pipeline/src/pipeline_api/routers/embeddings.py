from fastapi import APIRouter, UploadFile, Form
from ..utils.parse import parse_pdf
from ..schemas.embeddings import FileEmbeddingRequest
from ..utils.chunking import chunk_document
from ..utils.embedding import embed_chunks
from ..utils.db import add_vectors
import json

router = APIRouter(
    prefix="/embeddings",
    tags=["embeddings"],
)

@router.post("/documents")
async def embed_document(file: UploadFile, config: str = Form(...)):
    config_data = FileEmbeddingRequest(**json.loads(config))
    bytes = file.file
    elements = parse_pdf(bytes)
    chunks = chunk_document(elements=elements, chunking_strategy=config_data.chunking_strategy)
    embeddings = embed_chunks(chunks=chunks, embedding_model=config_data.model)
    add_vectors(collection_name=config_data.model, embeddings=embeddings, documents=chunks)
    return {"embeddings": embeddings.tolist()}
