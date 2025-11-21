from typing import List
from langchain_core.documents.base import Document
from .clients import clients
from sentence_transformers import SentenceTransformer
import numpy as np
from numpy.typing import NDArray
from fastapi import HTTPException, status

def embed_chunks(chunks: List[Document], embedding_model: str) -> NDArray[np.float32]:
    if not chunks:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No chunks provided for embedding")
    embeddings: List[List[float]] = []
    match embedding_model:
        case "openai_small":
            embeddings = embed_openai(chunks, model="text-embedding-3-small")
        case "openai_large":
            embeddings = embed_openai(chunks, model="text-embedding-3-large")
        case "huggingface_small":
            embeddings = embed_hugging_face(chunks, model="huggingface_small")
        case "huggingface_base":
            embeddings = embed_hugging_face(chunks, model="huggingface_base")
        case "huggingface_large":
            embeddings = embed_hugging_face(chunks, model="huggingface_large")
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported embedding model: {embedding_model}")
    
    return np.array(embeddings, dtype=np.float32)

def embed_openai(chunks: List[Document], model) -> List[List[float]]:
    response = clients["openai"].create(
        input=[chunk.page_content for chunk in chunks],
        model=model
    )
    return list(map(lambda res: res.embedding, response.data))

def embed_hugging_face(chunks: List[Document], model: str) -> List[List[float]]:
    hf_client: SentenceTransformer = clients[model]
    texts = [chunk.page_content for chunk in chunks]
    embeddings = hf_client.encode(texts, normalize_embeddings=True).tolist()
    return embeddings

def embed_texts(text: str, embedding_model: str) -> NDArray[np.float32]:
    if not text or not text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No text provided for embedding")
    embeddings: List[List[float]] = []
    match embedding_model:
        case "openai_small":
            embeddings = embed_text_openai([text], model="text-embedding-3-small")
        case "openai_large":
            embeddings = embed_text_openai([text], model="text-embedding-3-large")
        case "huggingface_small":
            embeddings = embed_text_hugging_face([text], model="huggingface_small")
        case "huggingface_base":
            embeddings = embed_text_hugging_face([text], model="huggingface_base")
        case "huggingface_large":
            embeddings = embed_text_hugging_face([text], model="huggingface_large")
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported embedding model: {embedding_model}") 
    return np.array(embeddings, dtype=np.float32)

def embed_text_openai(texts: List[str], model) -> List[List[float]]:
    response = clients["openai"].create(
        input=texts,
        model=model
    )
    return list(map(lambda res: res.embedding, response.data))

def embed_text_hugging_face(texts: List[str], model: str) -> List[List[float]]:
    hf_client: SentenceTransformer = clients[model]
    embeddings = hf_client.encode(texts, normalize_embeddings=True).tolist()
    return embeddings
