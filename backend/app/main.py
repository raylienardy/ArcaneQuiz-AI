from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.api.upload import router as upload_router
from app.api.ai import router as ai_router
from app.api.questions import router as questions_router
from app.api.export import router as export_router
import logging
from app.logging.formatter import JsonFormatter

settings = get_settings()

app = FastAPI(
    title="ArcaneQuiz AI",
    version="1.0.0",
    description="AI-powered question generation platform with magic theme",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # <-- sementara izinkan semua
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "Backend is running",
    }

# Register routers
app.include_router(upload_router)
app.include_router(ai_router)
app.include_router(questions_router)
app.include_router(export_router)

# Set handler untuk structured logging
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logging.getLogger("openquiz.generation").addHandler(handler)
logging.getLogger("openquiz.generation").setLevel(logging.INFO)