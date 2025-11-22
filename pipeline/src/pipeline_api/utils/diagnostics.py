from typing import List
from langchain_core.documents.base import Document
from .clients import base_hugging_face_client, openai_client
import numpy as np
import random
from .constants import SYNTHETIC_EVALUATION_PROMPT
import json

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
    
def perform_synthetic_query_diagnostics(chunks: List[Document], embedding_model, num_chunks: int = 8):
    testable_chunks = random.choices(chunks, k=num_chunks)
    testable_chunks = [f"{i}: {chunk.page_content}" for i, chunk in enumerate(testable_chunks)]
    chunks_string = "\n\n".join(testable_chunks)
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
        print(response)
    except json.JSONDecodeError:
        return {"error": "Response is not valid JSON", "response": response}
    return {"response": response}
    
    