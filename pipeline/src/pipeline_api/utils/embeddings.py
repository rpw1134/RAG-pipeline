from typing import List, Tuple
from contextlib import contextmanager
from langchain_core.documents.base import Document
from .clients import clients, chroma_client
from sentence_transformers import SentenceTransformer
import numpy as np
from numpy.typing import NDArray
from fastapi import HTTPException, status
import uuid
import time

def embed_chunks(chunks: List[Document], embedding_model: str) -> Tuple[NDArray[np.float32], float]:
    """
    Embed a list of Document chunks using the specified embedding model.

    Args:
        chunks: List of Document objects to embed.
        embedding_model: The embedding model to use (e.g., "openai_small", "huggingface_base").

    Returns:
        A numpy array of embeddings with shape (len(chunks), embedding_dim).

    Raises:
        HTTPException: If no chunks provided or model is unsupported.
    """
    if not chunks:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No chunks provided for embedding")
    embeddings: List[List[float]] = []
    start_time = time.time()
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
    
    time_taken = time.time() - start_time
    return np.array(embeddings, dtype=np.float32), time_taken

def embed_openai(chunks: List[Document], model) -> List[List[float]]:
    """
    Embed Document chunks using OpenAI's embedding API.

    Args:
        chunks: List of Document objects to embed.
        model: The OpenAI model name (e.g., "text-embedding-3-small").

    Returns:
        List of embedding vectors as lists of floats.
    """
    response = clients["openai"].create(
        input=[chunk.page_content for chunk in chunks],
        model=model
    )
    return list(map(lambda res: res.embedding, response.data))

def embed_hugging_face(chunks: List[Document], model: str) -> List[List[float]]:
    """
    Embed Document chunks using a HuggingFace SentenceTransformer model.

    Args:
        chunks: List of Document objects to embed.
        model: The client key for the HuggingFace model.

    Returns:
        List of normalized embedding vectors as lists of floats.
    """
    hf_client: SentenceTransformer = clients[model]
    texts = [chunk.page_content for chunk in chunks]
    embeddings = hf_client.encode(texts, normalize_embeddings=True).tolist()
    return embeddings

def embed_texts(text: str, embedding_model: str) -> NDArray[np.float32]:
    """
    Embed a single text string using the specified embedding model.

    Args:
        text: The text string to embed.
        embedding_model: The embedding model to use.

    Returns:
        A numpy array containing the embedding vector.

    Raises:
        HTTPException: If text is empty or model is unsupported.
    """
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
    """
    Embed text strings using OpenAI's embedding API.

    Args:
        texts: List of text strings to embed.
        model: The OpenAI model name.

    Returns:
        List of embedding vectors as lists of floats.
    """
    response = clients["openai"].create(
        input=texts,
        model=model
    )
    return list(map(lambda res: res.embedding, response.data))

def embed_text_hugging_face(texts: List[str], model: str) -> List[List[float]]:
    """
    Embed text strings using a HuggingFace SentenceTransformer model.

    Args:
        texts: List of text strings to embed.
        model: The client key for the HuggingFace model.

    Returns:
        List of normalized embedding vectors as lists of floats.
    """
    hf_client: SentenceTransformer = clients[model]
    embeddings = hf_client.encode(texts, normalize_embeddings=True).tolist()
    return embeddings


def batch_embed_texts(texts: List[str], embedding_model: str) -> NDArray[np.float32]:
    """
    Embed a batch of texts using the specified embedding model.

    Args:
        texts: List of text strings to embed.
        embedding_model: The embedding model to use.

    Returns:
        A numpy array of shape (len(texts), embedding_dim) with embeddings.
    """
    if not texts:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No texts provided for embedding")

    embeddings: List[List[float]] = []
    match embedding_model:
        case "openai_small":
            embeddings = embed_text_openai(texts, model="text-embedding-3-small")
        case "openai_large":
            embeddings = embed_text_openai(texts, model="text-embedding-3-large")
        case "huggingface_small":
            embeddings = embed_text_hugging_face(texts, model="huggingface_small")
        case "huggingface_base":
            embeddings = embed_text_hugging_face(texts, model="huggingface_base")
        case "huggingface_large":
            embeddings = embed_text_hugging_face(texts, model="huggingface_large")
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported embedding model: {embedding_model}")

    return np.array(embeddings, dtype=np.float32)


def cosine_similarity(a: NDArray[np.float32], b: NDArray[np.float32]) -> float:
    """
    Calculate cosine similarity between two vectors.
    For normalized vectors, this is equivalent to the dot product.
    """
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def pairwise_cosine_similarity(embeddings: NDArray[np.float32]) -> NDArray[np.float32]:
    """
    Calculate pairwise cosine similarity matrix for a set of embeddings.

    Args:
        embeddings: A numpy array of shape (n, embedding_dim).

    Returns:
        A numpy array of shape (n, n) containing pairwise cosine similarities.
    """
    # Normalize embeddings
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)  # Avoid division by zero
    normalized = embeddings / norms

    # Cosine similarity matrix is just the dot product of normalized vectors
    return np.dot(normalized, normalized.T)


def calculate_average_pairwise_similarity(embeddings: NDArray[np.float32]) -> float:
    """
    Calculate the average pairwise cosine similarity (redundancy score).
    Excludes self-similarity (diagonal) from the calculation.

    Args:
        embeddings: A numpy array of shape (n, embedding_dim).

    Returns:
        The average pairwise similarity (0 to 1). Higher = more redundant.
    """
    if len(embeddings) < 2:
        return 0.0

    sim_matrix = pairwise_cosine_similarity(embeddings)
    n = len(embeddings)

    # Get upper triangle (excluding diagonal) to avoid counting pairs twice
    upper_triangle = np.triu(sim_matrix, k=1)
    num_pairs = (n * (n - 1)) / 2

    return float(np.sum(upper_triangle) / num_pairs)


@contextmanager
def temporary_collection(embedding_model: str):
    """
    Context manager that creates a temporary ChromaDB collection and deletes it after use.

    Args:
        embedding_model: The embedding model name (used to generate a unique collection name).

    Yields:
        The temporary collection object.
    """
    collection_name = f"temp_{embedding_model}_{uuid.uuid4().hex[:8]}"
    collection = chroma_client.create_collection(collection_name)
    try:
        yield collection
    finally:
        chroma_client.delete_collection(collection_name)


