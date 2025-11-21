from FlagEmbedding import FlagReranker
from typing import List, Tuple
from ..types.embeddings import QueryResponse, RerankerResponse
import numpy as np

reranker: FlagReranker = FlagReranker("BAAI/bge-reranker-base")

def rerank_documents(query: str, query_results: QueryResponse , k: int )-> RerankerResponse:
    documents: List[str] = query_results.documents[0]
    pairs: List[Tuple[str,str]] = [(query, doc) for doc in documents]
    scores: np.ndarray | None = reranker.compute_score(pairs)
    if scores is None:
        raise ValueError("Reranker returned no scores")
    ranked_indices: List[int] = np.argsort(-scores)[:k].tolist()
    reranked_docs: List[str] = [documents[i] for i in ranked_indices]
    sorted_scores: List[float] = [float(scores[i]) for i in ranked_indices]
    return RerankerResponse(
        documents=reranked_docs,
        scores=sorted_scores
    )