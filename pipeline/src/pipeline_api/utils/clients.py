from openai import OpenAI
from sentence_transformers import SentenceTransformer
import os

openai_client: OpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
small_hugging_face_client = SentenceTransformer('BAAI/bge-small-en-v1.5')
base_hugging_face_client = SentenceTransformer('BAAI/bge-base-en-v1.5')
large_hugging_face_client = SentenceTransformer('BAAI/bge-large-en-v1.5')

clients = {
    "openai_small": openai_client.embeddings,
    "openai_large": openai_client.embeddings,
    "small_hugging_face": small_hugging_face_client,
    "base_hugging_face": base_hugging_face_client,
    "large_hugging_face": large_hugging_face_client,}