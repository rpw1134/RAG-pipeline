from pydantic import BaseModel
from typing import List

class FileEmbeddingRequest(BaseModel):
    model: str
    chunking_strategy: str
    # Synthetic query evaluation parameters
    run_chunk_diagnostics: bool = True
    run_synthetic_query_diagnostics: bool = True
    num_results: int = 10  # Number of vectors to retrieve from DB
    num_rerank: int = 5    # Number of documents to consider after reranking
    rerank: bool = True    # Whether to rerank or use directly retrieved vectors
    
class QueryEmbeddingRequest(BaseModel):
    query: str
    embedding_model: str
    llm_model: str
    rerank: bool = False
    num_queries: int = 10
    num_results: int = 5
    include_metadata: bool = True
    