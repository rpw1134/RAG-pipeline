from typing import List
from langchain_core.documents.base import Document
from .clients import clients


def embed_chunks(chunks: List[Document], embedding_model: str) -> List[List[float]]:
    embeddings: List[List[float]] = []
    if embedding_model == "openai_small":
        embeddings = embed_openai(chunks, model="text-embedding-3-small")
    return embeddings

def embed_openai(chunks: List[Document], model) -> List[List[float]]:
    response = clients["openai_small"].create(
        input=[chunk.page_content for chunk in chunks],
        model=model
    )
    return list(map(lambda res: res.embedding, response.data))
