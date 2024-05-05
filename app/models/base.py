from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]
strnotnull = Annotated[str, mapped_column(nullable=False)]


class BaseORM(DeclarativeBase):
    """Based sqlalchemy database model.

    Attributes
    ----------
    id: Any
        Element id

    """

    id: int
    __name__: str
    # Generate __tablename__ automatically

    # @declared_attr
    # def __tablename__(self) -> str:
    #     return self.__name__.lower()
