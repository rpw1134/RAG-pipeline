from typing import List
from langchain_core.documents.base import Document
from .clients import base_hugging_face_client
import numpy as np



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
    
def perform_synthetic_query_diagnostics(chunks: List[Document], embedding_model):
    pass