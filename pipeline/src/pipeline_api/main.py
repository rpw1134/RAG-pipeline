from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from .routers import embeddings, queries


app = FastAPI()
app.include_router(embeddings.router)
app.include_router(queries.router)
