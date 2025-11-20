from fastapi import FastAPI
from .utils.parse import parse_pdf
from .utils.chunking import chunk_document_elements_semantically, chunk_document_recursively, chunk_document_simply
from dotenv import load_dotenv
from .routers import embeddings

load_dotenv()
app = FastAPI()
app.include_router(embeddings.router)
