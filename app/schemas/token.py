from pydantic import BaseModel


class TokenRefreshModel(BaseModel):
    refresh: str


class TokenObtainPair(TokenRefreshModel):
    access: str
