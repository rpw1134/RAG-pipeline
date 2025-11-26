from FlagEmbedding import FlagReranker
from typing import List, Tuple
from ..types.embeddings import QueryResponse, RerankerResponse
import numpy as np
from chromadb.api.types import QueryResult
from fastapi import HTTPException, status

reranker: FlagReranker = FlagReranker("BAAI/bge-reranker-base")

def rerank_documents(query: str, query_results: QueryResult , k: int )-> RerankerResponse:
    """
    Rerank retrieved documents using a cross-encoder reranker model.

    Uses the BGE reranker to compute relevance scores between the query
    and each document, returning the top-k most relevant.

    Args:
        query: The query string to compare documents against.
        query_results: QueryResult from ChromaDB containing documents and metadata.
        k: Number of top documents to return after reranking.

    Returns:
        RerankerResponse with reranked documents and their scores.

    Raises:
        HTTPException: If no documents/metadata found or reranker fails.
    """
    docs_result = query_results.get("documents")
    if docs_result is None or len(docs_result) == 0 or len(docs_result[0]) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query results contain no documents")
    metadata_result = query_results.get("metadatas")
    if metadata_result is None or len(metadata_result) == 0 or len(metadata_result[0]) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query results contain no metadatas")
    documents: List[str] = docs_result[0]
    pairs: List[Tuple[str, str]] = [(query, doc) for doc in documents]
    num_pairs = len(pairs)
    if num_pairs== 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No document-query pairs to rerank")
    scores: np.ndarray | None = reranker.compute_score(pairs)
    if scores is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Reranker returned no scores")

    # Normalize reranker scores to [-1, 1] range to match cosine similarity scale
    # Using tanh to smoothly map unbounded scores to bounded range
    # Ensure scores is a numpy array for element-wise division
    scores_array = np.asarray(scores)
    normalized_scores = np.tanh(scores_array / 10.0)

    # Sort by descending score (highest relevance first) and take top k
    ranked_indices: List[int] = np.argsort(normalized_scores)[::-1][:k].tolist()
    reranked_docs: List[Tuple[str, dict]] = [(documents[i], dict(metadata_result[0][i])) for i in ranked_indices]
    sorted_scores: List[float] = [float(normalized_scores[i]) for i in ranked_indices]
    return RerankerResponse(
        documents=reranked_docs,
        scores=sorted_scores
    )
    
def format_documents(query_results: QueryResult) -> RerankerResponse:
    """
    Format query results into a RerankerResponse without reranking.

    Converts ChromaDB distances to similarity scores (1 - distance) and
    formats documents with their metadata.

    Args:
        query_results: QueryResult from ChromaDB containing documents,
                       metadata, and distances.

    Returns:
        RerankerResponse with formatted documents and similarity scores.

    Raises:
        HTTPException: If no documents, metadata, or distances found.
    """
    docs_result = query_results.get("documents")
    if docs_result is None or len(docs_result) == 0 or len(docs_result[0]) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query results contain no documents")
    metadata_result = query_results.get("metadatas")
    if metadata_result is None or len(metadata_result) == 0 or len(metadata_result[0]) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query results contain no metadatas")
    distances = query_results.get("distances")
    if distances is None or len(distances) == 0 or len(distances[0]) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query results contain no distances")
    scores: List[float] = [1 - d for d in distances[0]]
    documents: List[str] = docs_result[0]
    formatted_docs: List[Tuple[str, dict]] = [(documents[i], dict(metadata_result[0][i])) for i in range(len(documents))]
    return RerankerResponse(
        documents=formatted_docs,
        scores=scores
    )