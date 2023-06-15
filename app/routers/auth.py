from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.jwt import decode_refresh_token, encode_access_token, encode_refresh_token
from app.core.security import Hasher
from app.crud import get_user
from app.models.user import User
from app.schemas.token import TokenObtainPair, TokenRefreshModel
from app.schemas.user import UserCreateModel, UserLoginModel, UserResponseModel

auth_router = APIRouter(tags=["auth"])


@auth_router.post(
    "/signup", summary="User signup.", status_code=status.HTTP_201_CREATED, response_model=UserResponseModel
)
async def create_user(user: UserCreateModel, db_session: AsyncSession = Depends(get_db)) -> User:
    """Create new user.

    Parameters
    ----------
    user: UserCreateModel
        Pydantic model for user creation
    db_session: AsyncSession
        Asynchronous connection to database

    Returns
    -------
    new_user: User
        Sqlalchemy model with neccessary field, however it returns pydantic UserResponseModel

    """
    user_object = await get_user(user.email, db_session)
    if user_object:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exist")
    new_user = User(**{**user.dict(), "password": Hasher.get_password_hash(user.password)})
    await new_user.insert(db_session)
    return new_user


@auth_router.post(
    "/login",
    summary="User login.",
    status_code=status.HTTP_200_OK,
    response_model=TokenObtainPair,
)
async def login(user: UserLoginModel, database: AsyncSession = Depends(get_db)):
    """User login.

    Parameters
    ----------
    user: UserLoginModel
        Pydantic model for user sign in
    db_session: AsyncSession
        Asynchronous connection to database

    Returns
    -------
    TokenObtaionPair: Jwt token model with access and refresh tokens

    """
    executed_query = await database.execute(select(User.password).where(User.email == user.email))
    password_from_db = result[0] if (result := executed_query.fetchone()) else None
    if not password_from_db:
        #     # raise UserNotFoundException(user_email=user.email)
        raise SystemExit

    if not Hasher.verify_password(user.password, password_from_db):
        raise SystemExit
    #     # raise PasswordDoesNotMatchException

    refresh = encode_refresh_token(user_email=user.email)
    access = encode_access_token(user_email=user.email)

    return TokenObtainPair(access=access, refresh=refresh)


@auth_router.post(
    "/token/refresh",
    summary="Generates new access token via refresh token.",
    status_code=status.HTTP_200_OK,
    response_model=TokenObtainPair,
)
def refresh_access_token(token: TokenRefreshModel):
    """Refresh access token for jwt token.

    Parameters
    ----------
    token: TokenRefreshModel
        Pydantic model for refresh token

    Returns
    -------
    TokenObtaionPair: Jwt token model with access and refresh tokens

    """
    payload = decode_refresh_token(refresh_token=token.refresh)
    access = encode_access_token(user_email=payload["email"])

    return TokenObtainPair(access=access, refresh=token.refresh)
