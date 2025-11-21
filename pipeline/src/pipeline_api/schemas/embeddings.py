from pydantic import BaseModel
from typing import List

class FileEmbeddingRequest(BaseModel):
    model: str
    chunking_strategy: str
    
class QueryEmbeddingRequest(BaseModel):
    query: str
    model: str
    rerank: bool = False
    num_queries: int = 10
    num_results: int = 5
    include_metadata: bool = True