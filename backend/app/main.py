from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.api.upload import router as upload_router
from app.api.ai import router as ai_router   # <-- tambahan
from app.api.questions import router as questions_router   # tambahan
import logging
from app.logging.formatter import JsonFormatter
from app.api.export import router as export_router
from app.main import app


settings = get_settings()

app = FastAPI(
    title="OpenQuiz AI",
    version="1.0.0",
    description="AI-powered question generation platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://arcane-quiz-2ejj9mu75-alphocados-projects.vercel.app",  # <-- origin Vercel kamu
        "https://arcane-quiz-ai.vercel.app",  # <-- tambahkan juga domain utama nanti
    ],
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

app.include_router(upload_router)
app.include_router(ai_router)   # <-- tambahan
app.include_router(questions_router)
app.include_router(export_router)


# Set handler untuk logger kita
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logging.getLogger("openquiz.generation").addHandler(handler)
logging.getLogger("openquiz.generation").setLevel(logging.INFO)
