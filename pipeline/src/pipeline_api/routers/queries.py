from fastapi import APIRouter
from ..utils.db import query_top_k
from ..utils.embedding import embed_texts
from ..utils.reranking import rerank_documents, format_documents
from ..utils.llms import send_chat_request
from ..types.embeddings import RerankerResponse
from chromadb.api.types import QueryResult
from ..schemas.embeddings import QueryEmbeddingRequest

router = APIRouter(
    prefix="/queries",
    tags=["queries"],
)

@router.post("/")
async def query_endpoint(request: QueryEmbeddingRequest):
    embeddings = embed_texts(request.query, embedding_model=request.embedding_model)
    context: QueryResult = query_top_k(collection_name=request.embedding_model, embedding=embeddings, k=request.num_queries)
    docs_and_scores = RerankerResponse(documents=[], scores=[]) 
    if request.rerank:
        docs_and_scores: RerankerResponse = rerank_documents(request.query, query_results=context, k=request.num_results)
    else:
        docs_and_scores: RerankerResponse = format_documents(context)
    llm_response = send_chat_request(request.query, context=docs_and_scores, include_metadatas=request.include_metadata, model=request.llm_model)
    return {"results": docs_and_scores}