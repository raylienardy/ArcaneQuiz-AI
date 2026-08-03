import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.ai.providers import get_provider_registry
from app.ai.groq_client import GroqClient
from app.ai.models import AIRequest, AIResponse
from app.ai.exceptions import (
    AIAuthenticationError, AIRateLimitError, AITimeoutError,
    AIConnectionError, AIResponseError,
)
from groq import AuthenticationError, RateLimitError, APITimeoutError, APIError
from groq import APIConnectionError as GroqAPIConnectionError

from unittest.mock import MagicMock

def _make_groq_error(exc_class, message="Error"):
    """Buat instance exception Groq dengan response dan body tiruan."""
    response_mock = MagicMock()
    response_mock.status_code = 400
    response_mock.json.return_value = {"error": {"message": message}}
    return exc_class(
        message=message,
        response=response_mock,
        body={"error": {"message": message}}
    )

@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    monkeypatch.setattr("app.ai.groq_client.get_settings", lambda: MagicMock(
        groq_api_key="test-key", groq_model="test-model", ai_provider="groq"
    ))

@pytest.fixture
def groq_client():
    return GroqClient()

def test_registry_returns_groq_client():
    registry = get_provider_registry()
    client = registry.get_client("groq")
    assert isinstance(client, GroqClient)

@pytest.mark.asyncio
async def test_initialize_success(groq_client):
    with patch("app.ai.groq_client.AsyncGroq", autospec=True) as mock_groq:
        await groq_client.initialize()
        assert groq_client._client is not None
        mock_groq.assert_called_once_with(api_key="test-key")

@pytest.mark.asyncio
async def test_generate_maps_authentication_error(groq_client):
    groq_client._client = AsyncMock()
    groq_client._client.chat.completions.create.side_effect = _make_groq_error(AuthenticationError, "Invalid Key")
    with pytest.raises(AIAuthenticationError):
        await groq_client.generate(AIRequest(prompt="Test"))

@pytest.mark.asyncio
async def test_generate_maps_rate_limit_error(groq_client):
    groq_client._client = AsyncMock()
    groq_client._client.chat.completions.create.side_effect = _make_groq_error(RateLimitError, "Rate limit")
    with pytest.raises(AIRateLimitError):
        await groq_client.generate(AIRequest(prompt="Test"))

@pytest.mark.asyncio
async def test_generate_returns_ai_response(groq_client):
    groq_client._client = AsyncMock()
    groq_client._model_name = "test-model"
    mock_choice = MagicMock()
    mock_choice.message.content = "CONNECTED"
    mock_choice.finish_reason = "stop"
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_response.usage = MagicMock()
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 1
    mock_response.usage.total_tokens = 11
    groq_client._client.chat.completions.create.return_value = mock_response
    result = await groq_client.generate(AIRequest(prompt="Test"))
    assert isinstance(result, AIResponse)
    assert result.response_text == "CONNECTED"
    assert result.provider == "groq"
    assert result.metadata["model"] == "test-model"
    assert result.metadata["usage"]["total_tokens"] == 11