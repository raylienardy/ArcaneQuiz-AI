import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.question_service import QuestionService
from app.question_generator.models import QuestionRequest, QuestionType, DifficultyLevel
from app.ai.models import AIResponse

@pytest.fixture
def mock_ai_service():
    mock = AsyncMock()
    mock.initialize.return_value = None
    mock.generate.return_value = AIResponse(
        response_text='{"questions": [{"question": "What is 2+2?", "type": "multiple_choice", "choices": [{"label": "A", "text": "3"}, {"label": "B", "text": "4"}, {"label": "C", "text": "5"}, {"label": "D", "text": "6"}], "answer": "B", "explanation": "2+2=4"}]}',
        provider="mock",
        metadata={"model": "mock-model"}
    )
    return mock

@pytest.fixture
def question_service(mock_ai_service):
    with patch('app.services.question_service.AIService', return_value=mock_ai_service):
        service = QuestionService()
    return service

@pytest.mark.asyncio
async def test_pipeline_success(question_service):
    request = QuestionRequest(
        text="Some text",
        question_type=QuestionType.MULTIPLE_CHOICE,
        number_of_questions=1,
        difficulty=DifficultyLevel.EASY,
        language="en"
    )
    response = await question_service.generate_questions(request)
    assert len(response.questions) == 1
    assert response.questions[0].question == "What is 2+2?"
    assert response.provider == "mock"

@pytest.mark.asyncio
async def test_pipeline_parser_error(mock_ai_service):
    mock_ai_service.generate.return_value = AIResponse(
        response_text="Invalid JSON!!!",
        provider="mock",
        metadata={}
    )
    service = QuestionService()
    service.ai_service = mock_ai_service
    with pytest.raises(Exception):  # parser error
        await service.generate_questions(QuestionRequest(text="..", question_type=QuestionType.MULTIPLE_CHOICE, number_of_questions=1))