


from fastapi import APIRouter

router = APIRouter()

@router.get("/info")
def info():
    return { "application": "DevOps Lab API", "version": "0.1.0", "environment": "development"}

