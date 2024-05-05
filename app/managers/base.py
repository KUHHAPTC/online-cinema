from abc import ABC
from typing import ClassVar, Generic, List, Sequence

# from deprecated import deprecated
# from fastapi_pagination import Page
# from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import Select, delete, inspect, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DBAPIError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.roles import ColumnsClauseRole

from app.core.exceptions import BadRequestException, NotFoundException, raise_db_error
from app.models import GenericORM
from app.schemas import CreateSchema, UpdateSchema


class BaseManager(ABC, Generic[GenericORM, UpdateSchema, CreateSchema]):
    """Layer between database and service. Returns ORM object."""

    sql_model: ClassVar[GenericORM]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    # @staticmethod
    # # @deprecated
    # def apply_pagination(stmt: Select, filter_params: FilterParamsSchema) -> Select:
    #     """
    #     Apply pagination (limit and offset) parameters to the provided select statement.

    #     Args:
    #         stmt (Select): Provided statement.
    #         filter_params (FilterParamsSchema): FilterParamsSchema for filtering incoming query.

    #     Returns:
    #         Modified select statement.
    #     """
    #     if filter_params.limit:
    #         stmt = stmt.limit(filter_params.limit)

    #     if filter_params.offset:
    #         stmt = stmt.offset(filter_params.offset)

    #     return stmt

    # # @deprecated
    # def apply_ordering(self, stmt: Select, filter_params: FilterParamsSchema):
    #     """
    #     Apply the ordering for the provided statement.
    #     If no parameters are provided - default ordering is by `created_at` field.

    #     Args:
    #         stmt (Select): Provided statement.
    #         filter_params (FilterParamsSchema): FilterParamsSchema for filtering incoming query.

    #     Returns:
    #         Modified select statement.
    #     """
    #     if not filter_params.order_by:
    #         return stmt

    #     return stmt.order_by(getattr(self.sql_model, filter_params.order_by, self.sql_model.created_at))

    def get_query(self) -> Select:
        """
        Returns a query object for the model.

        :return: `Select` statement.
        """
        return select(self.sql_model)

    async def refresh(self, obj):
        await self.session.refresh(obj)

    async def get(self, obj_id: int) -> GenericORM:
        """
        Returns an object by its id.

        Args:
            obj_id (id): Object id.

        Returns:
            An Object.
        """
        query = self.get_query().where(self.sql_model.id == obj_id)

        result = await self.session.scalar(query)

        if not result:
            raise NotFoundException(detail=f"{self.sql_model.__name__} object with obj_id={obj_id} not found")

        return result

    # async def get_all(
    #     self, filter_params: FilterParamsSchema | BaseFilter, raw_result: bool = False
    # ) -> Page[Schema] | list[BaseORM]:
    #     """
    #     Returns all objects from the database.

    #     :param: filter_params (FilterParamsSchema): FilterParamsSchema for filtrating incoming query.
    #     :param: raw_result: If True, returns a list of raw results without pagination

    #     Returns:
    #         List of objects.
    #     """
    #     stmt = self.get_query()

    #     # Temporary. TODO: Remove after we will move to the new pagination flow.
    #     if not isinstance(filter_params, BaseFilter):
    #         stmt = self.apply_pagination(stmt, filter_params)
    #         stmt = self.apply_ordering(stmt, filter_params)

    #     elif isinstance(filter_params, BaseFilter):
    #         stmt = filter_params.filter(stmt)
    #         stmt = filter_params.sort(stmt)

    #     if raw_result:
    #         return (await self.session.scalars(stmt)).all()  # type: ignore

    #     return await paginate(self.session, stmt)

    async def get_by_ids(self, obj_ids: Sequence[int]) -> Sequence[GenericORM]:
        """
        Returns a list of objects by their ids.

        Args:
            obj_ids (Sequence[int]): List of ids.

        Returns:
            List of objects.
        """
        stmt = self.get_query().where(self.sql_model.id.in_(obj_ids))

        return (await self.session.scalars(stmt)).all()  # type: ignore

    async def _apply_changes(
        self,
        stmt,
        obj_id: int | None = None,
        *,
        is_unique: bool = False,
        flush: bool = False,
    ) -> GenericORM:
        """
        Internal method to store changes in DB
        """
        try:
            _result = await self.session.execute(stmt)

            if is_unique:
                _result = _result.unique()

            result: GenericORM = _result.scalar_one()

            if flush:
                await self.session.flush()
            else:
                await self.session.commit()

            await self.session.refresh(result)

        except DBAPIError as ex:
            await self.session.rollback()
            raise_db_error(ex)

        except NoResultFound as exc:
            raise NotFoundException(detail=f"{self.sql_model.__name__} object with obj_id={obj_id} not found") from exc

        return result

    async def create(self, obj: CreateSchema, flush: bool = False) -> GenericORM:
        """
        Creates an entity in the database and returns the created object.

        Args:
            obj (CreateSchema): The object to create.
            flush (bool, optional): If True, flush changes immediately, otherwise commit changes.

        Returns:
            The created object.
        """
        stmt = insert(self.sql_model).values(**obj.model_dump(exclude_defaults=True)).returning(self.sql_model)

        return await self._apply_changes(stmt=stmt, flush=flush)

    async def update(self, obj: UpdateSchema, obj_id: id, flush: bool = False) -> GenericORM:
        """
        Updates an object.

        Args:
            obj (UpdateSchema): The object to update.
            obj_id (int): The id of the object to update.
            flush (bool, optional): If True, flush changes immediately, otherwise commit changes.

        Returns:
            The updated object.
        """
        if not (updated_model := obj.model_dump(exclude_defaults=True)):
            raise BadRequestException("No data provided for updating")

        stmt = (
            update(self.sql_model).where(self.sql_model.id == obj_id).values(**updated_model).returning(self.sql_model)
        )

        return await self._apply_changes(stmt=stmt, obj_id=obj_id, flush=flush)

    async def delete(self, obj_id: int, flush: bool = False) -> None:
        """
        Delete an object.

        Args:
            obj_id (int): The id of the object to delete.
            flush (bool, optional): If True, perform an atomic delete (flush changes immediately),
                                     otherwise perform a permanent delete (commit changes).

        Raises:
            DBAPIError: If there is an error during database operations.
        """
        stmt = delete(self.sql_model).where(self.sql_model.id == obj_id)

        try:
            await self.session.execute(stmt)

            if flush:
                await self.session.flush()
            else:
                await self.session.commit()

        except DBAPIError as ex:
            await self.session.rollback()
            raise_db_error(ex)

    def get_select_entities(self, exclude_columns: List[str] | None = None) -> List[ColumnsClauseRole]:
        """
        Returns a list of SQLAlchemy column entities to be used in a SELECT statement.

        The method inspects the model's columns and constructs a list of SQLAlchemy column entities.
        It excludes the specified columns if provided.

        Args:
            exclude_columns (list[str], optional): Columns to be excluded from the result.

        Returns:
            list[ColumnsClauseRole]: A list of SQLAlchemy column entities.
        """
        exclude_columns = set(exclude_columns or [])

        mapper = inspect(self.sql_model)

        return [
            getattr(self.sql_model, entity.key)
            for entity in mapper.c
            if entity.key not in exclude_columns  # type: ignore
        ]
