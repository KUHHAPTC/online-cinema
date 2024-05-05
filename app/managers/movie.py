from typing import ClassVar, Type

from sqlalchemy import insert
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundException
from app.models import MovieORM, ReviewORM
from app.schemas import MovieCreateSchema

from .base import BaseManager


class MovieManager(BaseManager[MovieORM, MovieCreateSchema, MovieCreateSchema]):
    sql_model: ClassVar[Type[MovieORM]] = MovieORM

    async def create(self, obj: MovieCreateSchema, flush: bool = False) -> MovieORM:
        """
        Creates an entity in the database and returns the created object.

        Args:
            obj (MovieCreateSchema): The object to create.
            flush (bool, optional): If True, flush changes immediately, otherwise commit changes.

        Returns:
            The created object.
        """

        stmt = insert(self.sql_model).values(**obj.model_dump()).returning(self.sql_model)

        return await self._apply_changes(stmt=stmt, flush=flush)

    async def get_movie_with_reviews(self, movie_id: int) -> MovieORM:
        query = (
            self.get_query()
            .options(selectinload(self.sql_model.reviews).joinedload(ReviewORM.watcher))
            .filter(self.sql_model.id == movie_id)
        )
        result: MovieORM | None = await self.session.scalar(query)
        if not result:
            raise NotFoundException(detail=f"{self.sql_model.__name__} object with movie_id={movie_id} not found")
        return result
