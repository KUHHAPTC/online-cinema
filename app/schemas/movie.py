import datetime as dt
from typing import List

from pydantic import BaseModel, ConfigDict

from .user import UserResponseSchema


class MovieCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, revalidate_instances="always")

    title: str
    description: str = ""
    country: str
    budget: str
    year: int
    date_of_release: dt.date
    path_to_file: str = "/"


class MovieSchema(MovieCreateSchema):
    id: int


class MovieWatcherSchema(MovieCreateSchema):
    watcher: List["UserResponseSchema"] = []


# class UserMovieSchema(UserResponseSchema):
#     reviews: List["MovieCreateSchema"] = []

# genres: Mapped[List["GenreORM"]] = relationship(back_populates="movies", secondary="movies_genres")
# cast: Mapped[List["CastMemberORM"]] = relationship(back_populates="movies", secondary="movies_castmembers")
