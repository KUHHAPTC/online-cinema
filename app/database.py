# from sqlalchemy import create_engine
# import databases
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# logger = AppLogger.__call__().get_logger()
from app.config import Config
from app.models.base import Base

# from app import config
# import os

# global_settings = config.get_settings()
# USER_DB = os.environ.get("POSTGRES_USER")
# USER_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
# DB_NAME = os.environ.get("POSTGRES_DB")
# SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{USER_DB}:{USER_PASSWORD}@postgres/{DB_NAME}"


# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)

# async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Base = declarative_base()

# database = databases.Database(SQLALCHEMY_DATABASE_URL)

# metadata = sqlalchemy.MetaData()


# metadata.create_all(engine)


# from app.logging import AppLogger


engine = create_async_engine(
    Config.DB_CONFIG,
    future=True,
    echo=True,
)

# expire_on_commit=False will prevent attributes from being expired
# after commit.


async def get_db() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


# AsyncSessionFactory = sessionmaker(engine, autoflush=False, expire_on_commit=False, class_=AsyncSession)

# # Dependency
# async def get_db() -> AsyncGenerator:
#     async with AsyncSessionFactory() as session:
#         yield session


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
