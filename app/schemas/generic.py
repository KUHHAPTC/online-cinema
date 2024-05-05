from typing import TypeVar

from pydantic import BaseModel

Schema = TypeVar("Schema", bound=BaseModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
DeleteSchema = TypeVar("DeleteSchema", bound=BaseModel)
