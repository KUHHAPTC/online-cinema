from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseORM, intpk, strnotnull
from .enums import Role


class UserORM(BaseORM):
    """Sqlalchemy model of user."""

    __tablename__ = "users"

    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[strnotnull]
    first_name: Mapped[strnotnull]
    last_name: Mapped[str | None]
    role: Mapped[Role] = mapped_column(default=Role.USER)
    # watched_movies: Mapped[List["MovieORM"]] = relationship(back_populates="watchers", secondary="reviews")
    reviews: Mapped[List["ReviewORM"]] = relationship(back_populates="watcher")
