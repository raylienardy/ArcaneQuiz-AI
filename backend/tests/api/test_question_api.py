import pytest
from unittest.mock import patch, AsyncMock
from app.ai.models import AIResponse

def test_generate_endpoint_valid_request(client):
    with patch('app.services.question_service.QuestionService') as mock_service:
        instance = mock_service.return_value
        instance.generate_questions = AsyncMock()
        instance._last_prompt = "test"
        # Return a proper QuestionResponse
        from app.question_generator.models import QuestionResponse, Question, Choice, QuestionType
        instance.generate_questions.return_value = QuestionResponse(
            questions=[Question(
                id=1,
                question="What is AI?",
                type=QuestionType.MULTIPLE_CHOICE,
                choices=[Choice(label="A", text="A"), Choice(label="B", text="B"), Choice(label="C", text="C"), Choice(label="D", text="D")],
                answer="A",
                explanation="..."
            )],
            provider="mock",
            model="mock"
        )
        payload = {
            "text": "AI is...",
            "question_type": "multiple_choice",
            "number_of_questions": 1,
            "difficulty": "medium",
            "language": "en"
        }
        response = client.post("/questions/generate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert len(data["data"]["questions"]) == 1

def test_generate_endpoint_missing_fields(client):
    payload = {"text": "some text"}  # tidak ada question_type, number_of_questions
    response = client.post("/questions/generate", json=payload)
    assert response.status_code == 422  # validation error dari Pydantic