from abc import ABC
from typing import ClassVar, Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.managers import BaseManager
from app.schemas import CreateSchema, Schema

Manager = TypeVar("Manager", bound=BaseManager)


class BaseService(ABC, Generic[Manager, Schema, CreateSchema]):
    """Layer between managers and API."""

    manager_class: ClassVar[Manager]
    schema: ClassVar[Schema]

    def __init__(self, session: AsyncSession):
        self.db_session = session
        self.manager: Manager = self.manager_class(session)

    async def get(self, obj_id: int) -> Schema:
        result = await self.manager.get(obj_id=obj_id)

        return self.schema.model_validate(result)

    async def create(self, obj: CreateSchema) -> Schema:
        result = await self.manager.create(obj=obj)
        return self.schema.model_validate(result)
