from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseORM, intpk, strnotnull


class GenreORM(BaseORM):
    __tablename__ = "genres"

    id: Mapped[intpk]
    name: Mapped[strnotnull]
    description: Mapped[strnotnull]
    movies: Mapped[List["MovieORM"]] = relationship(back_populates="genres", secondary="movies_genres")


class MovieGenreORM(BaseORM):
    __tablename__ = "movies_genres"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)
