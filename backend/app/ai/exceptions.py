class AIConnectionError(Exception):
    """Failed to connect to AI provider."""
    pass

class AIAuthenticationError(Exception):
    """Invalid API key or authentication."""
    pass

class AIRateLimitError(Exception):
    """Rate limit exceeded."""
    pass

class AIResponseError(Exception):
    """Invalid or malformed response from provider."""
    pass

class AITimeoutError(Exception):
    """Request timed out."""
    pass

class ProviderNotSupportedError(Exception):
    """Requested provider is not registered."""
    pass