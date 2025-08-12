import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass(frozen=True)
class Settings:
    NEWSAPI_BASE_URL: str = os.getenv("NEWS_URL", "")
    NEWSAPI_KEY: str = os.getenv("NEWSAPI_KEY", "")

    HTTP_TIMEOUT: int = 15

settings = Settings()
