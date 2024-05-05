# from typing import Annotated
from fastapi import Depends  # , Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services import MovieService, ReviewService, UserService


async def get_user_service(
    session: AsyncSession = Depends(get_db),
):  # , authorization: Annotated[str | None, Header()] = None):
    return UserService(session=session)


async def get_movie_service(session: AsyncSession = Depends(get_db)):
    return MovieService(session=session)


async def get_review_service(session: AsyncSession = Depends(get_db)):
    return ReviewService(session=session)
