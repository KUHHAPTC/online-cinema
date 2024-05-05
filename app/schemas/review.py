from typing import List

from pydantic import BaseModel, ConfigDict

from .movie import MovieCreateSchema
from .user import UserResponseSchema


class ReviewBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, revalidate_instances="always")

    review_text: str | None = None
    rating: float | None = None


class ReviewCreateSchema(ReviewBaseSchema):
    user_id: int
    movie_id: int


class ReviewResponseSchema(ReviewBaseSchema):
    watcher: UserResponseSchema
    movie: MovieCreateSchema


class ReviewUserSchema(ReviewBaseSchema):
    movie: MovieCreateSchema


class ReviewMovieSchema(ReviewBaseSchema):
    watcher: UserResponseSchema


class UserReviewSchema(UserResponseSchema):
    reviews: List[ReviewUserSchema] = []


class MovieReviewSchema(MovieCreateSchema):
    reviews: List[ReviewMovieSchema] = []
