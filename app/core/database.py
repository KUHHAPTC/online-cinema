from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_db_settings

global_settings = get_db_settings()

engine = create_async_engine(
    global_settings.ASYNCPG_DSN,
    future=True,
    echo=True,
)

# expire_on_commit=False will prevent attributes from being expired after commit.
async def get_db() -> AsyncSession:
    """Create connection to database."""
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


# async def create_all():
#     """Create all tables in database after you save file with new class, without alembic migrations."""
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
