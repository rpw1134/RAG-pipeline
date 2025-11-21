from dataclasses import dataclass

@dataclass
class QueryResponse():
    ids: list[list[str]]
    embeddings: list[list[float]]
    documents: list[list[str]]
    included:list[str]
    metadatas: list[list[dict]]
    
@dataclass
class RerankerResponse():
    documents: list[str]
    scores: list[float]