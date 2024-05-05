from .generic import CreateSchema, DeleteSchema, Schema, UpdateSchema
from .movie import MovieCreateSchema, MovieSchema, MovieWatcherSchema
from .review import (
    MovieReviewSchema,
    ReviewBaseSchema,
    ReviewCreateSchema,
    ReviewMovieSchema,
    ReviewResponseSchema,
    ReviewUserSchema,
    UserReviewSchema,
)
from .token import TokenObtainPairSchema, TokenRefreshSchema
from .user import (
    UserCreateSchema,
    UserLoginSchema,
    UserResponseExtendedSchema,
    UserResponseSchema,
    UserSchema,
)

__all__ = [
    "TokenObtainPairSchema",
    "TokenRefreshSchema",
    "UserCreateSchema",
    "UserLoginSchema",
    "UserResponseSchema",
    "UserResponseExtendedSchema",
    "UserSchema",
    "MovieCreateSchema",
    "MovieWatcherSchema",
    "MovieSchema",
    "Schema",
    "CreateSchema",
    "UpdateSchema",
    "DeleteSchema",
    "ReviewBaseSchema",
    "ReviewCreateSchema",
    "UserReviewSchema",
    "MovieReviewSchema",
    "ReviewMovieSchema",
    "ReviewUserSchema",
    "ReviewResponseSchema",
]
