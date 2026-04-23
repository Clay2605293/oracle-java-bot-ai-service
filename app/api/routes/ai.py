from fastapi import APIRouter

router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/ping")
def ping_ai():
    return {
        "message": "AI route is working"
    }