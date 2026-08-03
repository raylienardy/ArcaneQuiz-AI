import pytest
from unittest.mock import patch, MagicMock
from app.services.ai_service import AIService
from app.ai.models import AIRequest, AIResponse
from unittest.mock import patch, MagicMock, AsyncMock

@pytest.mark.asyncio
async def test_ai_service_selects_groq(monkeypatch):
    monkeypatch.setattr("app.services.ai_service.get_settings", lambda: MagicMock(
        ai_provider="groq", groq_api_key="test-key", groq_model="test-model"
    ))
    mock_client = MagicMock()
    mock_client.generate = AsyncMock(return_value=AIResponse(response_text="Hello", provider="groq"))
    with patch("app.services.ai_service.get_provider_registry") as mock_registry:
        mock_registry.return_value.get_client.return_value = mock_client
        service = AIService()
        assert service.provider_name == "groq"
        result = await service.generate(AIRequest(prompt="Hi"))
        assert result.provider == "groq"
        assert result.response_text == "Hello"