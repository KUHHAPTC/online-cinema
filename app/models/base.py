from typing import Any

# from asyncpg import UniqueViolationError
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative  # , declared_attr


@as_declarative()
class Base:
    """Based sqlalchemy database model.

    Attributes
    ----------
    id: Any
        Element id

    Methods
    -------
    insert(db_session: AsyncSession):
        Insert value in database
    delete(db_session: AsyncSession):
        Remove value from database
    update(db_session: AsyncSession, **kwargs)
        Update values in database

    """

    id: Any
    __name__: str
    # Generate __tablename__ automatically

    # @declared_attr
    # def __tablename__(self) -> str:
    #     return self.__name__.lower()

    async def insert(self, db_session: AsyncSession) -> None:
        """Insert value in database.

        Parameters
        ----------
        db_session: AsyncSession
            Asynchronous connection to database

        Returns
        -------
        None

        """
        try:
            db_session.add(self)
            await db_session.commit()  # return None
        except IntegrityError as no_unique_key:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(no_unique_key)
            ) from no_unique_key
        except SQLAlchemyError as ex:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)) from ex

    async def delete(self, db_session: AsyncSession) -> None:
        """Delete value from database.

        Parameters
        ----------
        db_session: AsyncSession
            Asynchronous connection to database

        Returns
        -------
        None

        """
        try:
            await db_session.delete(self)
            await db_session.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)) from ex

    async def update(self, db_session: AsyncSession, **kwargs):
        """Update values in database.

        Parameters
        ----------
        db_session: AsyncSession
            Asynchronous connection to database
        kwargs:
            Values to update

        Returns
        -------
        None

        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        await self.insert(db_session)

    # async def save_or_update(self, db_sessions: AsyncSession):
    #     try:
    #         db_sessions.add(self)
    #         return await db_sessions.commit()
    #     except IntegrityError as exception:
    #         if isinstance(exception.orig, UniqueViolationError):
    #             return await db_sessions.merge(self)
    #         raise HTTPException(
    #             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #             detail=repr(exception),
    #         ) from exception
    #     finally:
    #         await db_sessions.close()
