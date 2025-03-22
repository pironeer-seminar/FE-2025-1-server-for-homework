from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.apps.router import api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(router=api_router)
