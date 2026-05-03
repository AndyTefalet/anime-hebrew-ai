"""Ani-Hebrew AI — FastAPI backend."""
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.transcribe import router as transcribe_router

app = FastAPI(title="Ani-Hebrew AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transcribe_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
