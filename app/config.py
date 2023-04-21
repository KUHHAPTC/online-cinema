import os

# from functools import lru_cache

# from pydantic import BaseSettings, PostgresDsn


# class Settings(BaseSettings):
#     asyncpg_url: PostgresDsn = PostgresDsn.build(
#         scheme="postgresql+asyncpg",
#         user=os.environ.get("POSTGRES_USER"),
#         password=os.environ.get("POSTGRES_PASSWORD"),
#         host="postgres",
#         port="5432",
#         path=os.environ.get("DB_NAME"),
#     )
# USER_DB = os.environ.get("POSTGRES_USER")
# USER_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
# DB_NAME = os.environ.get("POSTGRES_DB")

# @lru_cache
# def get_settings():
#     return Settings()


# settings = get_settings()


class Config:
    DB_USER = os.environ.get("POSTGRES_USER")
    DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    DB_NAME = os.environ.get("POSTGRES_DB")
    DB_HOST = os.environ.get("POSTGRES_HOST")
    DB_PORT = int(os.environ.get("POSTGRES_PORT", "5432"))
    DB_CONFIG = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
