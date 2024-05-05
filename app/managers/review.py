from typing import ClassVar, Type

from sqlalchemy.orm import joinedload

from app.core.exceptions import NotFoundException
from app.models import ReviewORM
from app.schemas import ReviewCreateSchema, ReviewResponseSchema

from .base import BaseManager


class ReviewManager(BaseManager[ReviewORM, ReviewResponseSchema, ReviewCreateSchema]):
    sql_model: ClassVar[Type[ReviewORM]] = ReviewORM

    async def get_review(self, movie_id: int, user_id: int) -> ReviewORM:
        query = (
            self.get_query()
            .options(joinedload(self.sql_model.movie))
            .options(joinedload(self.sql_model.watcher))
            .where(self.sql_model.movie_id == movie_id, self.sql_model.user_id == user_id)
        )
        result: ReviewORM | None = await self.session.scalar(query)
        if not result:
            raise NotFoundException(
                detail=f"{self.sql_model.__name__} object with movie_id={movie_id} and user_id={user_id} not found"
            )
        return result
