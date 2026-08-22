from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.root import router as root_router
from app.api.health import router as health_router
from app.api.info import router as info_router
from app.api.database import router as database_router
from app.api.users import router as users_router

from app.database.mongodb import create_indexes


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("\n      [FASTAPI] lifespan startup")
    print("      [FASTAPI] calling create_indexes()")

    create_indexes()

    print("      [FASTAPI] indexes ready")
    print("      [FASTAPI] application ready")

    yield

    print("      [FASTAPI] lifespan shutdown")


app = FastAPI(lifespan=lifespan)


app.include_router(root_router)
app.include_router(health_router)
app.include_router(info_router)
app.include_router(database_router)
app.include_router(users_router)