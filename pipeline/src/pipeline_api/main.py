from dotenv import load_dotenv
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .routers import embeddings, queries, collections


app = FastAPI()
app.include_router(embeddings.router)
app.include_router(queries.router)
app.include_router(collections.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

