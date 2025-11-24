from typing import List
from langchain_core.documents.base import Document
from .clients import base_hugging_face_client, openai_client
import numpy as np
import random
from .constants import SYNTHETIC_EVALUATION_PROMPT
import json
from ..utils.reranking import format_documents, rerank_documents
from fastapi import HTTPException, status
from .clients import collections
from .db import query_top_k
from .embeddings import embed_texts, batch_embed_texts, calculate_average_pairwise_similarity

def perform_chunk_diagnostics(chunks: List[Document]) -> dict:
    '''
    Perform diagnostics on the provided chunks to calculate average chunk length,
    average cohesion score, and average separation score.
    
    * Average Chunk Length: Precautionary measure. Extremes may indicate poor chunking and unreliable cohesion/separation scores.
    * Cohesion Score: Measures how semantically similar sentences within a chunk are to each other. Higher scores indicate better cohesion.
    * Separation Score: Measures how semantically different consecutive chunks are from each other. Lower scores indicate better separation.
    
    Ideals:
    1. Chunk length: 500-1500
    2. Cohesion score: 0.7-1.0
    3. Separation score: 0.1 to 0.4
    '''
    cohesion_scores = []
    seperation_scores = []
    chunk_lengths = 0
    average_chunk_length = 0

    if not chunks:
        return {
            "average_chunk_length": -1,
            "average_cohesion_score": -1,
            "average_seperation_score": -1
        }
    # cohesion score calculation
    for chunk in chunks:
        length = len(chunk.page_content)
        chunk_lengths += length
        sentences = chunk.page_content.split('.')
        sentence_embeddings = base_hugging_face_client.encode(
            sentences, normalize_embeddings=True
        )
        for i in range(1, len(sentence_embeddings)):
            cohesion = np.dot(sentence_embeddings[i], sentence_embeddings[i-1])/(np.linalg.norm(sentence_embeddings[i-1])*np.linalg.norm(sentence_embeddings[i]))
            cohesion_scores.append(cohesion)
    
    # seperation score calculation
    chunk_embeddings = base_hugging_face_client.encode(
        [chunk.page_content for chunk in chunks], normalize_embeddings=True
    )
    for i in range(1, len(chunk_embeddings)):
        seperation = np.dot(chunk_embeddings[i], chunk_embeddings[i-1])/(np.linalg.norm(chunk_embeddings[i-1])*np.linalg.norm(chunk_embeddings[i]))
        seperation_scores.append(seperation)
      
    # averages (convert to native Python floats for JSON serialization)
    average_chunk_length = float(chunk_lengths / len(chunks))
    average_cohesion_score = float(sum(cohesion_scores) / len(cohesion_scores)) if cohesion_scores else -1.0
    average_seperation_score = float(sum(seperation_scores) / len(seperation_scores)) if seperation_scores else -1.0

    return {
        "average_chunk_length": average_chunk_length,
        "average_cohesion_score": average_cohesion_score,
        "average_seperation_score": average_seperation_score
    }
    
def calculate_reciprocal_rank(expected_document: str, returned_documents: List[tuple]) -> float:
    """
    Calculate the reciprocal rank for a single query result.

    Args:
        expected_document: The document content that should be retrieved.
        returned_documents: List of (document_content, metadata) tuples in ranked order.

    Returns:
        The reciprocal rank (1/rank) if the expected document is found, 0.0 otherwise.
    """
    for rank, doc in enumerate(returned_documents, start=1):
        if doc[0] == expected_document:
            return 1.0 / rank
    return 0.0

def calculate_redundancy_score(documents: List[str], embedding_model: str) -> float:
    """
    Calculate the redundancy score between retrieved documents.

    Measures how similar the retrieved documents are to each other using
    pairwise cosine similarity. Higher scores indicate more redundant results.

    Args:
        documents: List of document text strings.
        embedding_model: The embedding model to use.

    Returns:
        The average pairwise similarity (0 to 1). Higher = more redundant.
    """
    if len(documents) < 2:
        return 0.0

    embeddings = batch_embed_texts(documents, embedding_model)
    return calculate_average_pairwise_similarity(embeddings)
    
def evaluate_synthetic_queries(
    queries: List[List[str]],
    documents: List[str],
    embedding_model: str,
    num_results: int = 10,
    num_rerank: int = 5,
    rerank: bool = True
) -> dict:
    """
    Evaluate retrieval quality using synthetic queries.

    Tests how well the retrieval system finds expected documents given
    synthetic queries that should return them.

    Args:
        queries: List of query groups where queries[i] should retrieve documents[i].
        documents: List of expected document contents to be retrieved.
        embedding_model: The embedding model/collection to query.
        num_results: Number of vectors to retrieve from the database.
        num_rerank: Number of documents to keep after reranking.
        rerank: Whether to apply reranking to results.

    Returns:
        Dict containing total_queries, hits, misses, hit_rate, and mrr.

    Raises:
        HTTPException: If embedding model is unknown or query/document counts mismatch.
    """
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
    reciprocal_ranks = []

    for i, query_group in enumerate(queries):
        expected_document = documents[i]
        doc_hits = 0
        doc_misses = 0
        doc_reciprocal_ranks = []

        for query in query_group:
            total_queries += 1

            # Embed the query
            query_embedding = embed_texts(query, embedding_model)

            # Query the collection with num_results
            results = query_top_k(
                collection_name=embedding_model,
                embedding=query_embedding,
                k=num_results
            )

            # Check if the expected document is in the returned documents
            raw_documents = results.get("documents")
            if not raw_documents:
                raise ValueError("No embedded documents")

            # Either rerank or format directly
            if rerank:
                returned_documents = rerank_documents(query, results, k=num_rerank)
            else:
                returned_documents = format_documents(results)

            returned_docs_list = list(returned_documents.documents)

            # Calculate reciprocal rank for this query
            rr = calculate_reciprocal_rank(expected_document, returned_docs_list)
            reciprocal_ranks.append(rr)
            doc_reciprocal_ranks.append(rr)

            if expected_document in list(map(lambda doc: doc[0], returned_docs_list)):
                hits += 1
                doc_hits += 1
            else:
                misses += 1
                doc_misses += 1

    hit_rate = hits / total_queries if total_queries > 0 else 0.0
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0.0

    return {
        "total_queries": total_queries,
        "hits": hits,
        "misses": misses,
        "hit_rate": hit_rate,
        "mrr": mrr,
    }
    
    
def perform_synthetic_query_diagnostics(chunks: List[Document], embedding_model, num_chunks: int = 8, num_results : int = 5, num_rerank:int = 5, rerank: bool = True) -> dict:
    """
    Run synthetic query diagnostics on a set of document chunks.

    Randomly samples chunks, generates synthetic queries using an LLM,
    and evaluates how well the retrieval system finds the original chunks.

    Args:
        chunks: List of Document objects to sample from.
        embedding_model: The embedding model/collection to query.
        num_chunks: Number of chunks to randomly sample for testing.
        num_results: Number of vectors to retrieve from the database.
        num_rerank: Number of documents to keep after reranking.
        rerank: Whether to apply reranking to results.

    Returns:
        Dict containing hit_rate, mrr, and other diagnostic metrics,
        or an error dict if LLM response parsing fails.
    """
    testable_chunks = random.choices(chunks, k=num_chunks)
    # Keep original page_content for DB comparison
    original_contents = [chunk.page_content for chunk in testable_chunks]
    # Add index prefix only for LLM prompt
    indexed_chunks = [f"{i}: {chunk.page_content}" for i, chunk in enumerate(testable_chunks)]
    chunks_string = "\n\n".join(indexed_chunks)
    reply = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": SYNTHETIC_EVALUATION_PROMPT + "\n\n" + chunks_string
            },
        ]
    )
    if not reply.choices or not reply.choices[0].message.content:
        return {"error": "No content in chat completion response"}
    response = reply.choices[0].message.content
    try:
        response = json.loads(response)
    except json.JSONDecodeError:
        return {"error": "Response is not valid JSON", "response": response}

    res = evaluate_synthetic_queries(queries=response, documents=original_contents, embedding_model=embedding_model, num_results=num_results, num_rerank=num_rerank, rerank=rerank)
    return res
    
    