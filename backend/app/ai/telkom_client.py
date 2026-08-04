"""
Telkom LLM Client – integrasi dengan Telkom AI DAG via OpenAI-compatible API.
Menggunakan httpx untuk request HTTP asinkron.
"""

import logging
from typing import Optional
import httpx

from .base_client import BaseAIClient
from .models import AIRequest, AIResponse
from .exceptions import (
    AIAuthenticationError,
    AIConnectionError,
    AIRateLimitError,
    AIResponseError,
    AITimeoutError,
)
from ..config import get_settings

logger = logging.getLogger(__name__)

TELKOM_BASE_URL = "https://telkom-ai-dag.api.apilogy.id/Telkom-LLM/0.0.4"


class TelkomLLMClient(BaseAIClient):
    """Implementasi Telkom LLM menggunakan httpx."""

    def __init__(self, key_number: int = 1):
        self._client: Optional[httpx.AsyncClient] = None
        self._model_name: Optional[str] = None
        self._initialized = False
        self._key_number = key_number  # 1 sampai 5

    async def initialize(self) -> None:
        if self._initialized:
            return

        settings = get_settings()
        # Ambil API key sesuai nomor
        api_key_map = {
            1: settings.telkom_api_key_1,
            2: settings.telkom_api_key_2,
            3: settings.telkom_api_key_3,
            4: settings.telkom_api_key_4,
            5: settings.telkom_api_key_5,
        }
        api_key = api_key_map.get(self._key_number, "").strip()
        self._model_name = settings.telkom_model.strip() or "telkom-ai"

        if not api_key:
            raise AIAuthenticationError(
                f"Telkom API key #{self._key_number} is missing. "
                f"Set TELKOM_API_KEY_{self._key_number} in environment variables."
            )

        try:
            self._client = httpx.AsyncClient(
                base_url=TELKOM_BASE_URL,
                headers={
                    "x-api-key": api_key,
                    "Content-Type": "application/json",
                },
                timeout=60.0,
            )
            self._initialized = True
            logger.info(f"Telkom LLM client #{self._key_number} initialized for model '{self._model_name}'.")
        except Exception as e:
            raise AIConnectionError(
                f"Failed to initialize Telkom LLM client #{self._key_number}: {str(e)}"
            ) from e

    async def generate(self, request: AIRequest) -> AIResponse:
        if not self._client:
            raise AIConnectionError(f"Telkom LLM client #{self._key_number} not initialized.")

        payload = {
            "model": self._model_name,
            "messages": [{"role": "user", "content": request.prompt}],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": False,
        }

        try:
            response = await self._client.post("/llm/chat/completions", json=payload)
        except httpx.TimeoutException as e:
            raise AITimeoutError(f"Telkom LLM #{self._key_number} request timed out.") from e
        except httpx.ConnectError as e:
            raise AIConnectionError(f"Telkom LLM #{self._key_number} connection failed: {str(e)}") from e

        # Tangani error HTTP
        if response.status_code == 401:
            raise AIAuthenticationError(f"Telkom LLM #{self._key_number}: Invalid API key.")
        elif response.status_code == 429:
            raise AIRateLimitError(f"Telkom LLM #{self._key_number}: Rate limit exceeded.")
        elif response.status_code >= 500:
            raise AIResponseError(
                f"Telkom LLM #{self._key_number}: Server error ({response.status_code})."
            )

        # Parse respons JSON
        try:
            data = response.json()
        except Exception as e:
            raise AIResponseError(
                f"Telkom LLM #{self._key_number}: Failed to parse JSON response: {str(e)}"
            ) from e

        # Ekstrak teks dari respons
        choices = data.get("choices", [])
        if not choices:
            raise AIResponseError(f"Telkom LLM #{self._key_number}: Empty choices in response.")

        response_text = choices[0].get("message", {}).get("content", "")
        finish_reason = choices[0].get("finish_reason", "unknown")

        logger.info(f"Telkom LLM #{self._key_number} response received.")
        return AIResponse(
            response_text=response_text,
            provider=f"telkom{self._key_number}",
            metadata={
                "model": self._model_name,
                "finish_reason": finish_reason,
            },
        )

    async def health_check(self) -> bool:
        if not self._client:
            return False
        try:
            req = AIRequest(prompt="Ping", max_tokens=5)
            resp = await self.generate(req)
            return bool(resp.response_text)
        except Exception:
            return False

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
        self._initialized = False
        logger.info(f"Telkom LLM client #{self._key_number} closed.")