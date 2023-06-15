from enum import IntEnum, auto
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserRole(IntEnum):
    AUTHORIZED = auto()  # 1
    ADMIN = auto()


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: Optional[str] = None


class UserCreateModel(UserBase):
    password: str = Field(..., min_length=4)


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str


class UserResponseModel(UserBase):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserResponseModelExtended(UserBase):
    id: int
    role: UserRole

    @property
    def is_authorized(self):
        return self.role == UserRole.AUTHORIZED

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN
