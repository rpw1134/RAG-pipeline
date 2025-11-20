from pydantic import BaseModel
from typing import List

class FileEmbeddingRequest(BaseModel):
    model: str
    chunking_strategy: str
    
class QueryEmbeddingRequest(BaseModel):
    queries: List[str]
    model: str