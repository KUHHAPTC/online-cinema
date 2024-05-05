from fastapi import APIRouter, Depends, Header, status

from app.dependencies import get_user_service
from app.schemas import UserResponseSchema, UserReviewSchema, UserSchema
from app.services import UserService

user_router = APIRouter(tags=["users"])


@user_router.get("/me", summary="User page.", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def retrieve_current_user(
    authorization: str = Header(...), user_service: UserService = Depends(get_user_service)
) -> UserSchema:
    """Retrieve current user.

    Parameters
    ----------
    authorization: str
        Header 'authorization' with jwt token
    user_service: UserService
        Service for user operations

    Returns
    -------
    user: UserResponseSchema
        Pydantic model of user

    """
    user = await user_service.get_current_user(authorization)
    return user


@user_router.get("/me/movies", summary="User page.", status_code=status.HTTP_200_OK, response_model=UserReviewSchema)
async def get_user_with_movies(
    authorization: str = Header(...), user_service: UserService = Depends(get_user_service)
) -> UserReviewSchema:
    """Retrieve current user with movies he watched.

    Parameters
    ----------
    authorization: str
        Header 'authorization' with jwt token
    user_service: UserService
        Service for user operations

    Returns
    -------
    user: UserReviewSchema
        Pydantic model of user with his movies

    """
    user = await user_service.get_current_user_with_movies(authorization)
    return user
