from fastapi.routing import APIRouter
from app.apps import user
from app.apps import todo

api_router = APIRouter(prefix="/api")
api_router.include_router(user.router)
api_router.include_router(todo.router)
