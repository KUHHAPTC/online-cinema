from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseORM, intpk, strnotnull
from .enums import MovieRole


class CastMemberORM(BaseORM):
    __tablename__ = "castmembers"

    id: Mapped[intpk]
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[strnotnull]
    description: Mapped[strnotnull]
    age: Mapped[int]
    role: Mapped[MovieRole]
    movies: Mapped[List["MovieORM"]] = relationship(back_populates="cast", secondary="movies_castmembers")


class MovieCastMemberORM(BaseORM):
    __tablename__ = "movies_castmembers"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    castmember_id: Mapped[int] = mapped_column(ForeignKey("castmembers.id", ondelete="CASCADE"), primary_key=True)
