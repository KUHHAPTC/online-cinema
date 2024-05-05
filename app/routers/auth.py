from fastapi import APIRouter, Depends, status

from app.core.exceptions import InvalidCredentialsException
from app.core.jwt import decode_refresh_token, encode_access_token, encode_refresh_token
from app.core.security import Hasher
from app.dependencies import get_user_service
from app.schemas import (
    TokenObtainPairSchema,
    TokenRefreshSchema,
    UserCreateSchema,
    UserLoginSchema,
    UserResponseSchema,
)
from app.services.user import UserService

auth_router = APIRouter(tags=["auth"])


@auth_router.post(
    "/signup", summary="User signup.", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema
)
async def create_user(user_create: UserCreateSchema, user_service: UserService = Depends(get_user_service)):
    """Create new user.

    Parameters
    ----------
    user_create: UserCreateModel
        Pydantic model for user creation
    user_service: UserService
        Service for user operations

    Returns
    -------
    user: UserResponseSchema
        Inserted user model without password

    """
    await user_service.is_user_exist(email=user_create.email)
    user_create.password = Hasher.get_password_hash(user_create.password)
    user = await user_service.create(obj=user_create)
    return user


@auth_router.post(
    "/login",
    summary="User login.",
    status_code=status.HTTP_200_OK,
    response_model=TokenObtainPairSchema,
)
async def login(user: UserLoginSchema, user_service: UserService = Depends(get_user_service)):
    """User login.

    Parameters
    ----------
    user: UserLoginModel
        Pydantic model for user sign in
    user_service: UserService
        Service for user operations

    Returns
    -------
    TokenObtainPairSchema: Jwt token model with access and refresh tokens

    """
    exist_user = await user_service.get_user_by_email(email=user.email)

    if not Hasher.verify_password(user.password, exist_user.password):
        raise InvalidCredentialsException

    refresh = encode_refresh_token(user_email=user.email)
    access = encode_access_token(user_email=user.email)

    return TokenObtainPairSchema(access=access, refresh=refresh)


@auth_router.post(
    "/token/refresh",
    summary="Generates new access token via refresh token.",
    status_code=status.HTTP_200_OK,
    response_model=TokenObtainPairSchema,
)
def refresh_access_token(token: TokenRefreshSchema):
    """Refresh access token for jwt token.

    Parameters
    ----------
    token: TokenRefreshModel
        Pydantic model for refresh token

    Returns
    -------
    TokenObtaionPairSchema: Jwt token model with access and refresh tokens

    """
    payload = decode_refresh_token(refresh_token=token.refresh)
    access = encode_access_token(user_email=payload["email"])

    return TokenObtainPairSchema(access=access, refresh=token.refresh)
