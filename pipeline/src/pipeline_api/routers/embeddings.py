from fastapi import APIRouter, UploadFile, Form
from ..utils.parse import parse_pdf
from ..schemas.embeddings import FileEmbeddingRequest
from ..utils.chunking import chunk_document
from ..utils.embeddings import embed_chunks
from ..utils.db import add_vectors
from ..utils.diagnostics import perform_chunk_diagnostics, perform_synthetic_query_diagnostics
from ..utils.db import collections
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
    diagnostics = {}
    if config_data.run_chunk_diagnostics:
        diagnostics['chunk'] = perform_chunk_diagnostics(chunks=chunks)
    embeddings = embed_chunks(chunks=chunks, embedding_model=config_data.model)
    add_vectors(collection_name=config_data.model, embeddings=embeddings, documents=chunks)
    if config_data.run_synthetic_query_diagnostics:
        diagnostics['synthetic'] = perform_synthetic_query_diagnostics(chunks=chunks,embedding_model=config_data.model, num_results=config_data.num_results,num_rerank=config_data.num_rerank, rerank=config_data.rerank
    )
    
    return {"diagnostics": diagnostics, "num_chunks": len(chunks)}

