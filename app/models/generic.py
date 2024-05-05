from typing import TypeVar

from .base import BaseORM

GenericORM = TypeVar("GenericORM", bound=BaseORM)
