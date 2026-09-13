
import os

from fastapi import APIRouter, HTTPException


router = APIRouter()


@router.get("/health")
def health():

    force_health_fail = os.getenv(
        "FORCE_HEALTH_FAIL",
        "false"
    ).lower() == "true"

    if force_health_fail:
        raise HTTPException(
            status_code=500,
            detail="Intentional health check failure"
        )

    return {
        "status": "ok"
    }