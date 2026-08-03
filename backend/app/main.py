from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ArcaneQuiz AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Backend is running"}

# Import router
from app.api.upload import router as upload_router
from app.api.questions import router as questions_router
from app.api.export import router as export_router
from app.api.ai import router as ai_router

app.include_router(upload_router)
app.include_router(questions_router)
app.include_router(export_router)
app.include_router(ai_router)