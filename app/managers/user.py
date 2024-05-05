from typing import ClassVar, Type

from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundException, UserExistsException
from app.models import ReviewORM, UserORM
from app.schemas import UserCreateSchema, UserResponseExtendedSchema

from .base import BaseManager

# m2o and o2o - joinedload | o2m and m2m - selectinload


class UserManager(BaseManager[UserORM, UserResponseExtendedSchema, UserCreateSchema]):
    sql_model: ClassVar[Type[UserORM]] = UserORM

    async def _get_user_by_email(self, email: str) -> UserORM | None:
        query = self.get_query().where(self.sql_model.email == email)
        return await self.session.scalar(query)

    async def get_by_email(self, email: str) -> UserORM:
        result: UserORM | None = await self._get_user_by_email(email)
        if not result:
            raise NotFoundException(detail=f"{self.sql_model.__name__} object with email={email} not found")

        return result

    async def is_user_exist(self, email: str) -> None:
        result: UserORM | None = await self._get_user_by_email(email)

        if result:
            raise UserExistsException(email)

    async def get_user_with_movies(self, email: str) -> UserORM:
        query = (
            self.get_query()
            .options(selectinload(self.sql_model.reviews).joinedload(ReviewORM.movie))
            .where(self.sql_model.email == email)
        )
        result = await self.session.scalar(query)
        return result
