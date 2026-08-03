from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    ESSAY = "essay"
    TRUE_FALSE = "true_false"

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Choice(BaseModel):
    label: str = Field(..., description="Label pilihan, e.g., A, B, C, D")
    text: str = Field(..., description="Teks pilihan")
    is_correct: Optional[bool] = Field(None, description="True jika ini jawaban benar (untuk multiple choice)")

class Question(BaseModel):
    id: Optional[int] = None
    question: str = Field(..., description="Teks pertanyaan")
    type: QuestionType = Field(..., description="Tipe pertanyaan")
    choices: Optional[List[Choice]] = Field(None, description="Pilihan (untuk multiple choice)")
    answer: Optional[str] = Field(None, description="Jawaban benar (teks atau label)")
    explanation: Optional[str] = Field(None, description="Penjelasan jawaban")
    difficulty: Optional[DifficultyLevel] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class QuestionRequest(BaseModel):
    text: str = Field(..., description="Teks sumber (dokumen yang diekstrak)")
    question_type: QuestionType
    number_of_questions: int = Field(..., ge=1, le=50)
    difficulty: Optional[DifficultyLevel] = None
    language: str = "id"  # default Indonesia
    additional_instruction: Optional[str] = None
    # Tempat untuk ekspansi masa depan (Bloom, learning objectives, tags, dll.)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class QuestionResponse(BaseModel):
    questions: List[Question] = Field(default_factory=list)
    provider: str = ""
    model: str = ""
    generation_time: Optional[float] = None  # dalam detik
    metadata: Dict[str, Any] = Field(default_factory=dict)