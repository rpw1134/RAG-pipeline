from pydantic import BaseModel

class FileEmbeddingRequest(BaseModel):
    model: str
    chunking_strategy: str
    