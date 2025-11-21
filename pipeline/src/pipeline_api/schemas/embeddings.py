from pydantic import BaseModel
from typing import List

class FileEmbeddingRequest(BaseModel):
    model: str
    chunking_strategy: str
    
class QueryEmbeddingRequest(BaseModel):
    query: str
    model: str
    rerank: bool = False
    num_results: int = 5