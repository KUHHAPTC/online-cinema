from enum import IntEnum, auto
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserRole(IntEnum):
    AUTHORIZED = auto()  # 1
    ADMIN = auto()


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: Optional[str]


class UserCreateModel(UserBase):
    email: EmailStr
    first_name: str
    last_name: Optional[str] = None
    password: str = Field(..., min_length=4)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserLoginModel(BaseModel):
    email: str
    password: str


class UserIdModel(BaseModel):
    user_id: int


class UserResponseModel(UserBase):
    email: str
    first_name: str
    last_name: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserResponseModelExtended(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: Optional[str]
    role: UserRole

    @property
    def is_authorized(self):
        return self.role == UserRole.AUTHORIZED

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN
