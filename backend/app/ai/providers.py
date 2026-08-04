from typing import Dict, Type
from .base_client import BaseAIClient
from .telkom_client import TelkomLLMClient


class AIProviderRegistry:
    def __init__(self):
        self._providers: Dict[str, Type[BaseAIClient]] = {
            "telkom1": TelkomLLMClient,
            "telkom2": TelkomLLMClient,
            "telkom3": TelkomLLMClient,
            "telkom4": TelkomLLMClient,
            "telkom5": TelkomLLMClient,
        }

    def get_client(self, provider_name: str) -> BaseAIClient:
        name = provider_name.lower()
        # Ekstrak nomor dari nama (telkom1 -> 1, telkom2 -> 2, dst)
        if name.startswith("telkom"):
            try:
                num = int(name.replace("telkom", ""))
                if 1 <= num <= 5:
                    return TelkomLLMClient(key_number=num)
            except ValueError:
                pass
        # Fallback ke dictionary (untuk provider lain jika ada)
        provider_class = self._providers.get(name)
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
        return list(self._providers.keys())


_provider_registry = None


def get_provider_registry() -> AIProviderRegistry:
    global _provider_registry
    if _provider_registry is None:
        _provider_registry = AIProviderRegistry()
    return _provider_registry