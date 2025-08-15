import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    NEWSAPI_BASE_URL: str = os.getenv("NEWSAPI_BASE_URL", "")
    NEWSAPI_KEY: str = os.getenv("NEWSAPI_KEY", "")
    JWT_SECRET: str = Field(default="change-me")
    HTTP_TIMEOUT: int = os.getenv("HTTP_TIMEOUT", 15)
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "")

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()

