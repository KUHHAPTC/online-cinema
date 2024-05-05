import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseORM, intpk, strnotnull


class MovieORM(BaseORM):
    __tablename__ = "movies"

    id: Mapped[intpk]
    title: Mapped[strnotnull]
    description: Mapped[strnotnull]
    country: Mapped[str]
    budget: Mapped[str]
    year: Mapped[int]
    date_of_release: Mapped[datetime.date] = mapped_column(nullable=False)
    path_to_file: Mapped[strnotnull]
    # watchers: Mapped[List["UserORM"]] = relationship(back_populates="watched_movies", secondary="reviews")
    reviews: Mapped[List["ReviewORM"]] = relationship(back_populates="movie")
    genres: Mapped[List["GenreORM"]] = relationship(back_populates="movies", secondary="movies_genres")
    cast: Mapped[List["CastMemberORM"]] = relationship(back_populates="movies", secondary="movies_castmembers")


class ReviewORM(BaseORM):
    __tablename__ = "reviews"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    rating: Mapped[float | None]
    review_text: Mapped[str | None]

    watcher: Mapped["UserORM"] = relationship(back_populates="reviews")  # , viewonly=True)
    movie: Mapped["MovieORM"] = relationship(back_populates="reviews")  # , viewonly=True)
