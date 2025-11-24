from fastapi import APIRouter, Query
from ..utils.clients import collections

router = APIRouter(
    prefix="/collections",
    tags=["collections"],
)

@router.get("/")
async def list_collections(active_only: bool = Query(True, description="If true, only return collections with data")):
    """
    List all available collections.

    Args:
        active_only: If true, only return collections that have data.

    Returns:
        A list of collection names.
    """
    if active_only:
        return {"collections": [name for name, col in collections.items() if col.count() > 0]}
    else:
        return {"collections": list(collections.keys())}
    
@router.delete("/{collection_name}")
async def delete_collection(collection_name: str):
    if collection_name in collections:
        collection = collections[collection_name]
        collection.delete()
        return {"detail": f"Collection {collection_name} cleared"}
    else:
        return {"detail": f"Collection {collection_name} does not exist"}