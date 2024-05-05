from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import Role


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, revalidate_instances="always")

    email: EmailStr
    first_name: str
    last_name: str | None = None


class UserCreateSchema(UserResponseSchema):
    password: str = Field(..., min_length=4)


class UserResponseExtendedSchema(UserResponseSchema):
    id: int
    role: Role

    @property
    def is_admin(self):
        return self.role == Role.ADMIN


class UserSchema(UserResponseExtendedSchema):
    password: str = Field(..., min_length=4)
