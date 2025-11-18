from typing import List
from langchain_core.documents.base import Document


def embed_chunks(chunks: List[Document], embedding_model: str) -> List[List[float]]:
    embeddings: List[List[float]] = []
    return embeddings

