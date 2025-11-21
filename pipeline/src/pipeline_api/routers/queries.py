from fastapi import APIRouter
from ..utils.db import query_top_k
from ..utils.embedding import embed_texts
from ..utils.reranking import rerank_documents
from ..types.embeddings import RerankerResponse
from chromadb.api.types import QueryResult
from ..schemas.embeddings import QueryEmbeddingRequest

router = APIRouter(
    prefix="/queries",
    tags=["queries"],
)

@router.post("/")
async def query_endpoint(request: QueryEmbeddingRequest):
    embeddings = embed_texts(request.query, embedding_model=request.model)
    context: QueryResult = query_top_k(collection_name=request.model, embedding=embeddings, k=request.num_results)
    docs_and_scores = RerankerResponse(documents=[], scores=[]) 
    if request.rerank:
        docs_and_scores: RerankerResponse = rerank_documents(request.query, query_results=context, k=request.num_results)
        return {"results": docs_and_scores}
    return {"results": context, "rerank": docs_and_scores}