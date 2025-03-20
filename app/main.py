import os
from fastapi import FastAPI
from app.apps.router import api_router

app = FastAPI()

app.include_router(router=api_router)
