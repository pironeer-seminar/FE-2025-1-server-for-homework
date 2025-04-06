from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.apps.router import api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
            "http://localhost:5173",
            "https://homework-fe-2025-1-week3-navy.vercel.app",
            "https://homework-fe-2025-1-week3-navy.vercel.app"
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(router=api_router)
