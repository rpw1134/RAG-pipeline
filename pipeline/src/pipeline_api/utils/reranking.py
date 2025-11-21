from FlagEmbedding import FlagReranker
from typing import List, Tuple
from ..types.embeddings import QueryResponse, RerankerResponse
import numpy as np
from chromadb.api.types import QueryResult

reranker: FlagReranker = FlagReranker("BAAI/bge-reranker-base")

def rerank_documents(query: str, query_results: QueryResult , k: int )-> RerankerResponse:
    docs_result = query_results.get("documents")
    if docs_result is None or len(docs_result) == 0 or len(docs_result[0]) == 0:
        raise ValueError("Query results contain no documents")
    metadata_result = query_results.get("metadatas")
    if metadata_result is None or len(metadata_result) == 0 or len(metadata_result[0]) == 0:
        raise ValueError("Query results contain no metadatas")
    documents: List[str] = docs_result[0]
    pairs: List[Tuple[str, str]] = [(query, doc) for doc in documents]
    num_pairs = len(pairs)
    if num_pairs== 0:
        raise ValueError("No document-query pairs to rerank")
    scores: np.ndarray | None = reranker.compute_score(pairs)
    print(scores)
    if scores is None:
        raise ValueError("Reranker returned no scores")
    # Sort by descending score (highest relevance first) and take top k
    ranked_indices: List[int] = np.argsort(scores)[::-1][:k].tolist()
    reranked_docs: List[Tuple[str, dict]] = [(documents[i], dict(metadata_result[0][i])) for i in ranked_indices]
    sorted_scores: List[float] = [float(scores[i]) for i in ranked_indices]
    print(sorted_scores)
    return RerankerResponse(
        documents=reranked_docs,
        scores=sorted_scores
    )
    
def format_documents(query_results: QueryResult) -> RerankerResponse:
    docs_result = query_results.get("documents")
    if docs_result is None or len(docs_result) == 0 or len(docs_result[0]) == 0:
        raise ValueError("Query results contain no documents")
    metadata_result = query_results.get("metadatas")
    if metadata_result is None or len(metadata_result) == 0 or len(metadata_result[0]) == 0:
        raise ValueError("Query results contain no metadatas")
    distances = query_results.get("distances")
    if distances is None or len(distances) == 0 or len(distances[0]) == 0:
        raise ValueError("Query results contain no distances")
    scores: List[float] = [1 - d for d in distances[0]]
    documents: List[str] = docs_result[0]
    formatted_docs: List[Tuple[str, dict]] = [(documents[i], dict(metadata_result[0][i])) for i in range(len(documents))]
    return RerankerResponse(
        documents=formatted_docs,
        scores=scores
    )