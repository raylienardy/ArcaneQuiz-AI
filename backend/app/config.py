from pydantic_settings import BaseSettings
from pydantic import ConfigDict, field_validator
from functools import lru_cache

SUPPORTED_PROVIDERS = ["telkom1", "telkom2", "telkom3", "telkom4", "telkom5"]

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # AI Provider (wajib)
    ai_provider: str

    @field_validator("ai_provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        v_lower = v.lower().strip()
        if v_lower not in SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported AI provider '{v}'. "
                f"Supported providers: {', '.join(SUPPORTED_PROVIDERS)}."
            )
        return v_lower
      
    telkom_api_key_1: str = ""

    telkom_api_key_2: str = ""

    telkom_api_key_3: str = ""

    telkom_api_key_4: str = ""

    telkom_api_key_5: str = ""

    telkom_model: str = "telkom-ai"
    
    # CORS
    cors_origins: list[str] = ["http://localhost:5173"]

    # File upload
    max_upload_size: int = 20 * 1024 * 1024
    allowed_extensions: list[str] = [".pdf", ".docx", ".txt"]


@lru_cache()
def get_settings() -> Settings:
    return Settings()