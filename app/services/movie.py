from typing import ClassVar, Type

from app.managers import MovieManager
from app.schemas import MovieCreateSchema, MovieReviewSchema, MovieSchema

from .base import BaseService


class MovieService(BaseService[MovieManager, MovieSchema, MovieCreateSchema]):
    manager_class: ClassVar[Type[MovieManager]] = MovieManager
    schema: ClassVar[Type[MovieSchema]] = MovieSchema

    async def get_movie_with_reviews(self, movie_id: int) -> MovieReviewSchema:
        movies = await self.manager.get_movie_with_reviews(movie_id)
        print(f"{movies.__dict__=}")
        return MovieReviewSchema.model_validate(movies)
