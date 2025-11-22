from typing import List
from langchain_core.documents.base import Document
from .clients import clients, collections
from .db import query_top_k
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

def evaluate_synthetic_queries(queries: List[List[str]], documents: List[str], embedding_model: str) -> dict:
    if embedding_model not in collections:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown embedding model: {embedding_model}"
        )

    if len(queries) != len(documents):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Number of query groups ({len(queries)}) must match number of documents ({len(documents)})"
        )

    total_queries = 0
    hits = 0
    misses = 0
    results_by_document = []

    for i, query_group in enumerate(queries):
        expected_document = documents[i]
        doc_hits = 0
        doc_misses = 0

        for query in query_group:
            total_queries += 1

            # Embed the query
            query_embedding = embed_texts(query, embedding_model)

            # Query the collection with k=5
            results = query_top_k(
                collection_name=embedding_model,
                embedding=query_embedding,
                k=5
            )

            # Check if the expected document is in the returned documents
            returned_documents = results.get("documents")
            if not returned_documents:
                raise ValueError("No embedded documents")
            
            returned_documents = returned_documents[0] if results.get("documents") else []

            if expected_document in returned_documents:
                hits += 1
                doc_hits += 1
            else:
                misses += 1
                doc_misses += 1

        results_by_document.append({
            "document_index": i,
            "num_queries": len(query_group),
            "hits": doc_hits,
            "misses": doc_misses,
            "hit_rate": doc_hits / len(query_group) if query_group else 0.0
        })

    hit_rate = hits / total_queries if total_queries > 0 else 0.0

    return {
        "total_queries": total_queries,
        "hits": hits,
        "misses": misses,
        "hit_rate": hit_rate,
        "results_by_document": results_by_document
    }
