from datetime import timedelta
from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """Settings for fastapi application."""

    ASYNCPG_URL: PostgresDsn  # takes value from .env file

    JWT_TOKEN_PREFIX: str = "Bearer"
    ACCESS_TOKEN_LIFETIME: timedelta = timedelta(days=31)
    REFRESH_TOKEN_LIFETIME: timedelta = timedelta(days=365)
    ALGORITHM: str = "HS256"


@lru_cache
def get_settings() -> Settings:
    """Get settings for application."""
    return Settings()
