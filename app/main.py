


from fastapi import FastAPI

from app.api.root import router as root_router
from app.api.health import router as health_router
from app.api.info import router as info_router 
from app.api.database import router as database_router
from app.api.users import router as users_router

app = FastAPI()


app.include_router(root_router)
app.include_router(health_router)
app.include_router(info_router)
app.include_router(database_router)
app.include_router(users_router)