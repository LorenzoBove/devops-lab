from fastapi import APIRouter

from app.database.mongodb import client


router = APIRouter()


@router.get("/database")
def database_status():
    client.admin.command("ping")

    return {
        "database": "ok"
    }