from typing import ClassVar, Type

from app.managers import ReviewManager
from app.schemas import ReviewBaseSchema, ReviewCreateSchema, ReviewResponseSchema

from .base import BaseService


class ReviewService(BaseService[ReviewManager, ReviewResponseSchema, ReviewCreateSchema]):
    manager_class: ClassVar[Type[ReviewManager]] = ReviewManager
    schema: ClassVar[Type[ReviewResponseSchema]] = ReviewResponseSchema

    async def create_review(self, movie_id: int, user_id: int, review: ReviewBaseSchema) -> ReviewCreateSchema:
        review_object = {"movie_id": movie_id, "user_id": user_id, **review.model_dump(exclude_none=True)}
        review_create = ReviewCreateSchema(**review_object)
        # result = await super().create(obj=review_create)
        result = await self.manager.create(review_create)
        return ReviewCreateSchema.model_validate(result)

    async def get_review(self, movie_id: int, user_id: int) -> ReviewResponseSchema:
        review = await self.manager.get_review(movie_id, user_id)
        return self.schema.model_validate(review)
