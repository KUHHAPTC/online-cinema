from datetime import timedelta
from functools import lru_cache

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    """Settings for Postgres database."""

    POSTGRES_SCHEME: str = "postgresql+asyncpg"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    @property
    def ASYNCPG_DSN(self) -> str:
        connection_string: PostgresDsn = PostgresDsn.build(
            scheme=self.POSTGRES_SCHEME,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            path=self.POSTGRES_DB,
        )
        return connection_string.unicode_string()


class CacheSettings(BaseSettings):
    """Settings for fastapi application."""

    REDIS_SCHEME: str = "redis"
    REDIS_PASSWORD: str
    REDIS_HOST: str

    @property
    def REDIS_DSN(self) -> str:
        connection_string: RedisDsn = RedisDsn.build(
            scheme=self.REDIS_SCHEME,
            password=self.REDIS_PASSWORD,
            host=self.REDIS_HOST,
        )
        return connection_string.unicode_string()


class JWTSettings(BaseSettings):

    SECRET: str  # takes value from .secret.env file
    JWT_TOKEN_PREFIX: str = "Bearer"
    ACCESS_TOKEN_LIFETIME: timedelta = timedelta(days=31)
    REFRESH_TOKEN_LIFETIME: timedelta = timedelta(days=365)
    ALGORITHM: str = "HS256"


@lru_cache
def get_jwt_settings() -> JWTSettings:
    """Get JWT settings for application."""
    return JWTSettings()


@lru_cache
def get_db_settings() -> DBSettings:
    """Get database settings for application."""
    return DBSettings()


@lru_cache
def get_cache_settings() -> CacheSettings:
    """Get cache settings for application."""
    return CacheSettings()
