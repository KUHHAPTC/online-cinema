from typing import ClassVar, Type

from app.core.cache import cache
from app.core.jwt import parse_authorization_token
from app.managers import UserManager
from app.schemas import UserCreateSchema, UserReviewSchema, UserSchema

from .base import BaseService


class UserService(BaseService[UserManager, UserSchema, UserCreateSchema]):
    manager_class: ClassVar[Type[UserManager]] = UserManager
    schema: ClassVar[Type[UserSchema]] = UserSchema

    @cache(model=UserSchema, expire=300)
    async def get_user_by_email(self, email: str) -> UserSchema:

        result = await self.manager.get_by_email(email=email)
        return self.schema.model_validate(result)

    async def is_user_exist(self, email: str) -> None:

        await self.manager.is_user_exist(email=email)

    @cache(model=UserSchema, expire=300)
    async def get_current_user(self, token: str) -> UserSchema:
        """Get current user.

        Parameters
        ----------
        token: str
            Jwt access token
        database: AsyncSession
            Asynchronous connection to database

        Returns
        -------
        user: UserResponseExtendedModel
            Pydantic user model presented for viewing

        """
        payload = parse_authorization_token(token)
        user_email = payload["email"]

        user = await self.get_user_by_email(email=user_email)
        return user

    async def get_current_user_with_movies(self, token: str) -> UserReviewSchema:
        """Get current user.

        Parameters
        ----------
        token: str
            Jwt access token
        database: AsyncSession
            Asynchronous connection to database

        Returns
        -------
        user: UserReviewSchema
            Pydantic user model presented for viewing with movies

        """
        payload = parse_authorization_token(token)
        user_email = payload["email"]

        user_with_movies = await self.manager.get_user_with_movies(user_email)
        return UserReviewSchema.model_validate(user_with_movies)
