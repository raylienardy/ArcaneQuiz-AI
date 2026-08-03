from typing import Dict, Type
from .base_client import BaseAIClient
from .gemini_client import GeminiClient
from .groq_client import GroqClient
from .mock_client import MockClient

class AIProviderRegistry:
    def __init__(self):
        self._providers: Dict[str, Type[BaseAIClient]] = {
            "gemini": GeminiClient,
            "groq": GroqClient,
            "mock": MockClient,   # <-- tambahan
        }

    def get_client(self, provider_name: str) -> BaseAIClient:
        provider_class = self._providers.get(provider_name.lower())
        if not provider_class:
            from .exceptions import ProviderNotSupportedError
            raise ProviderNotSupportedError(
                f"Provider '{provider_name}' is not supported. "
                f"Available: {', '.join(self.supported_providers())}."
            )
        return provider_class()

    def register(self, name: str, client_class: Type[BaseAIClient]) -> None:
        self._providers[name.lower()] = client_class

    def supported_providers(self) -> list[str]:
        """Kembalikan daftar nama provider yang terdaftar."""
        return list(self._providers.keys())

_provider_registry = None

def get_provider_registry() -> AIProviderRegistry:
    global _provider_registry
    if _provider_registry is None:
        _provider_registry = AIProviderRegistry()
    return _provider_registry