import os
from fastapi import FastAPI
from app.apps.router import api_router
from dotenv import load_dotenv

if os.getenv("ENVIRONMENT") == "production":
    load_dotenv(".env.prod")
else:
    load_dotenv(".env.dev")
app = FastAPI()

app.include_router(router=api_router)
