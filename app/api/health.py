


from fastapi import APIRouter, HTTPException


router = APIRouter()

@router.get("/health")
def health():
    return {"status" : "ok"}

"""


router = APIRouter()

@router.get("/health")
def health():
    raise HTTPException(
        status_code=500,
        detail="Intentional health check failure"
    )



"""