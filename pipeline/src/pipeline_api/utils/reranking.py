from FlagEmbedding import FlagReranker
from typing import List, Tuple
from ..types.embeddings import QueryResponse, RerankerResponse
import numpy as np
from chromadb.api.types import QueryResult

reranker: FlagReranker = FlagReranker("BAAI/bge-reranker-base")

def rerank_documents(query: str, query_results: QueryResult , k: int )-> RerankerResponse:
    docs_result = query_results.get("documents")
    if docs_result is None or len(docs_result) == 0:
        raise ValueError("Query results contain no documents")
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
    reranked_docs: List[str] = [documents[i] for i in ranked_indices]
    sorted_scores: List[float] = [float(scores[i]) for i in ranked_indices]
    print(sorted_scores)
    return RerankerResponse(
        documents=reranked_docs,
        scores=sorted_scores
    )