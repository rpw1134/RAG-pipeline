from fastapi import APIRouter
from ..utils.db import query_top_k
from ..utils.embedding import embed_texts
from ..schemas.embeddings import QueryEmbeddingRequest

router = APIRouter(
    prefix="/queries",
    tags=["queries"],
)

@router.post("/")
async def query_endpoint(request: QueryEmbeddingRequest):
    embeddings = embed_texts(request.queries, embedding_model=request.model)
    context = query_top_k(collection_name=request.model, embedding=embeddings, k=5)
    return {"results": context}