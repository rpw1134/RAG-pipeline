from langchain_core.documents.base import Document
from chromadb import Collection
from .clients import collections
from uuid import uuid4 as uuid
from numpy.typing import NDArray
import numpy as np
from typing import List
from chromadb.api.types import QueryResult
from fastapi import HTTPException, status

def add_vectors(collection_name: str, embeddings: NDArray[np.float32], documents: list[Document]):
    """
    Add document vectors to a ChromaDB collection.

    Args:
        collection_name: The name of the collection to add vectors to.
        embeddings: A numpy array of embeddings with shape (n, embedding_dim).
        documents: List of Document objects containing page_content and metadata.

    Raises:
        HTTPException: If collection is unknown, no embeddings/documents provided,
                       or counts don't match.
    """
    if collection_name not in collections:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unknown collection: {collection_name}")
    if len(embeddings) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No embeddings provided")
    if len(documents) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No documents provided")
    if len(embeddings) != len(documents):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Embeddings count ({len(embeddings)}) does not match documents count ({len(documents)})")

    collection: Collection = collections[collection_name]
    collection.add(
        ids=[str(uuid()) for i in range(len(embeddings))],
        embeddings=embeddings,
        documents=[document.page_content for document in documents],
        metadatas=[document.metadata for document in documents],
    )

def query_top_k(collection_name: str, embedding: NDArray[np.float32], k: int) -> QueryResult:
    """
    Query a ChromaDB collection for the top-k most similar documents.

    Args:
        collection_name: The name of the collection to query.
        embedding: The query embedding vector.
        k: The number of results to return.

    Returns:
        QueryResult containing documents, metadatas, and distances.

    Raises:
        HTTPException: If collection is unknown or k is not positive.
    """
    if collection_name not in collections:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unknown collection: {collection_name}")
    if k <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="k must be a positive integer")

    collection: Collection = collections[collection_name]
    results = collection.query(
        query_embeddings=embedding,
        n_results=k
    )
    return results
    