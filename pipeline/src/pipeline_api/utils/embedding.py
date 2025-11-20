from typing import List
from langchain_core.documents.base import Document
from .clients import clients
from sentence_transformers import SentenceTransformer
import numpy as np
from numpy.typing import NDArray

def embed_chunks(chunks: List[Document], embedding_model: str) -> NDArray[np.float32]:
    embeddings: List[List[float]] = []
    match embedding_model:
        case "openai_small":
            embeddings = embed_openai(chunks, model="text-embedding-3-small")
        case "openai_large":
            embeddings = embed_openai(chunks, model="text-embedding-3-large")
        case "small_hugging_face":
            embeddings = embed_hugging_face(chunks, model="small_hugging_face")
        case "base_hugging_face":
            embeddings = embed_hugging_face(chunks, model="base_hugging_face")
        case "large_hugging_face":
            embeddings = embed_hugging_face(chunks, model="large_hugging_face")
        case _:
            raise ValueError(f"Unsupported embedding model: {embedding_model}")
    
    return np.array(embeddings, dtype=np.float32)

def embed_openai(chunks: List[Document], model) -> List[List[float]]:
    response = clients["openai_small"].create(
        input=[chunk.page_content for chunk in chunks],
        model=model
    )
    return list(map(lambda res: res.embedding, response.data))

def embed_hugging_face(chunks: List[Document], model: str) -> List[List[float]]:
    hf_client: SentenceTransformer = clients[model]
    texts = [chunk.page_content for chunk in chunks]
    embeddings = hf_client.encode(texts, normalize_embeddings=True).tolist()
    return embeddings
