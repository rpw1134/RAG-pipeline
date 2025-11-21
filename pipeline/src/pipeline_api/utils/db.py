from langchain_core.documents.base import Document
from chromadb import Collection
from .clients import collections
from uuid import uuid4 as uuid
from numpy.typing import NDArray
import numpy as np
from typing import List
from chromadb.api.types import QueryResult

def add_vectors(collection_name: str, embeddings: NDArray[np.float32], documents: list[Document]):
    collection: Collection = collections[collection_name]
    collection.add(
        ids=[str(uuid()) for i in range(len(embeddings))],
        embeddings=embeddings,
        documents=[document.page_content for document in documents],
        metadatas=[document.metadata for document in documents],
    )
    
def query_top_k(collection_name: str, embedding: NDArray[np.float32], k:int) -> QueryResult:
    collection: Collection = collections[collection_name]
    results = collection.query(
        query_embeddings=embedding,
        n_results=k
    )
    return results
    