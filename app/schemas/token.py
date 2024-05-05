from pydantic import BaseModel


class TokenRefreshSchema(BaseModel):
    refresh: str


class TokenObtainPairSchema(TokenRefreshSchema):
    access: str
