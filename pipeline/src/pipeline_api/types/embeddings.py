from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class QueryResponse():
    ids: list[list[str]]
    embeddings: list[list[float]]
    documents: list[list[str]]
    included:list[str]
    metadatas: list[list[dict]]
    
@dataclass
class RerankerResponse():
    documents: List[Tuple[str, dict]]
    scores: list[float]