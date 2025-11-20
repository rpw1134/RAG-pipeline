from fastapi import APIRouter

router = APIRouter(
    prefix="/queries",
    tags=["queries"],
)

@router.post("/")
async def query_endpoint():
    pass