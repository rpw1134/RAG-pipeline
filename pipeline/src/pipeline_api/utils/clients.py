from openai import OpenAI
from sentence_transformers import SentenceTransformer
import os
from chromadb import Client

chroma_client = Client()
openai_small_collection = chroma_client.create_collection("openai_small_embeddings")
openai_large_collection = chroma_client.create_collection("openai_large_embeddings")
bge_small_collection = chroma_client.create_collection("bge_small_embeddings")
bge_base_collection = chroma_client.create_collection("bge_base_embeddings")
bge_large_collection = chroma_client.create_collection("bge_large_embeddings")

openai_client: OpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
small_hugging_face_client: SentenceTransformer = SentenceTransformer('BAAI/bge-small-en-v1.5')
base_hugging_face_client: SentenceTransformer = SentenceTransformer('BAAI/bge-base-en-v1.5')
large_hugging_face_client: SentenceTransformer = SentenceTransformer('BAAI/bge-large-en-v1.5', device='mps')

clients = {
    "openai": openai_client.embeddings,
    "huggingface_small": small_hugging_face_client,
    "huggingface_base": base_hugging_face_client,
    "huggingface_large": large_hugging_face_client,}

collections = {
    "openai_small": openai_small_collection,
    "openai_large": openai_large_collection,
    "huggingface_small": bge_small_collection,
    "huggingface_base": bge_base_collection,
    "huggingface_large": bge_large_collection,
}