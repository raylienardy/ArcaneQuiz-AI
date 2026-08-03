import logging
import time
from typing import Optional
from groq import AsyncGroq, APIError, AuthenticationError, RateLimitError, APITimeoutError
from groq import APIConnectionError as GroqAPIConnectionError

from .base_client import BaseAIClient
from .models import AIRequest, AIResponse
from .exceptions import (
    AIAuthenticationError, AIConnectionError, AIRateLimitError,
    AIResponseError, AITimeoutError,
)
from ..config import get_settings

logger = logging.getLogger(__name__)

class GroqClient(BaseAIClient):
    def __init__(self):
        self._client: Optional[AsyncGroq] = None
        self._model_name: Optional[str] = None
        self._initialized = False   # <-- tambahan

    async def initialize(self) -> None:
        if self._client:
            return
        if self._initialized:
            return
        settings = get_settings()
        api_key = settings.groq_api_key.strip()
        self._model_name = settings.groq_model.strip()
        if not api_key:
            raise AIAuthenticationError("Groq API key is missing. Set GROQ_API_KEY in .env.")
        if not self._model_name:
            raise AIConnectionError("Groq model is not configured. Set GROQ_MODEL in .env.")
        try:
            self._client = AsyncGroq(api_key=api_key)
            self._initialized = True
            logger.info(f"Groq client initialized for model '{self._model_name}'.")
        except Exception as e:
            raise AIConnectionError(f"Failed to initialize Groq client: {str(e)}") from e

    async def generate(self, request: AIRequest) -> AIResponse:
        if not self._client:
            raise AIConnectionError("Groq client not initialized.")
        start_time = time.time()
        logger.info("Groq request started.")
        try:
            response = await self._client.chat.completions.create(
                model=self._model_name,
                messages=[{"role": "user", "content": request.prompt}],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )
            latency = int((time.time() - start_time) * 1000)
            response_text = response.choices[0].message.content if response.choices else ""
            metadata = {
                "model": self._model_name,
                "finish_reason": response.choices[0].finish_reason if response.choices else None,
                "latency_ms": latency,
            }
            if hasattr(response, 'usage') and response.usage:
                metadata["usage"] = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                }
            logger.info(f"Groq response received in {latency}ms.")
            return AIResponse(response_text=response_text, provider="groq", metadata=metadata)
        except AuthenticationError as e:
            raise AIAuthenticationError(str(e)) from e
        except RateLimitError as e:
            raise AIRateLimitError(str(e)) from e
        except APITimeoutError as e:
            raise AITimeoutError(str(e)) from e
        except GroqAPIConnectionError as e:
            raise AIConnectionError(str(e)) from e
        except APIError as e:
            raise AIResponseError(str(e)) from e
        except Exception as e:
            raise AIConnectionError(f"Unexpected error: {str(e)}") from e

    async def health_check(self) -> bool:
        """Health check menggunakan prompt kecil (memakai token)."""
        if not self._client:
            return False
        try:
            req = AIRequest(prompt="Ping", max_tokens=5)
            resp = await self.generate(req)
            return bool(resp.response_text)
        except Exception:
            return False

    async def close(self) -> None:
        self._client = None