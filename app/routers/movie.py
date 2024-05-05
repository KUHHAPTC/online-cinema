from fastapi import APIRouter, Depends, Header, status

from app.dependencies import get_movie_service, get_review_service, get_user_service
from app.schemas import (
    MovieCreateSchema,
    MovieReviewSchema,
    MovieSchema,
    ReviewBaseSchema,
    ReviewCreateSchema,
    ReviewResponseSchema,
)
from app.services import MovieService, ReviewService, UserService

movie_router = APIRouter(tags=["movies"])


@movie_router.get(
    "/{movie_id}", summary="Movie data by id.", status_code=status.HTTP_200_OK, response_model=MovieCreateSchema
)
async def get_movie(movie_id: int, movie_service: MovieService = Depends(get_movie_service)):
    """Get movie.

    Parameters
    ----------
    movie_id: int
        Movie id
    movie_service: MovieService
        Service for movie operations

    Returns
    -------
    movie: MovieBaseSchema
        Movie model

    """
    movie = await movie_service.get(movie_id)
    return movie


@movie_router.post(
    "/add", summary="Add movie in db.", status_code=status.HTTP_201_CREATED, response_model=MovieCreateSchema
)
async def add_movie(
    movie_scheme: MovieCreateSchema, movie_service: MovieService = Depends(get_movie_service)
) -> MovieSchema:
    """Create new movie.

    Parameters
    ----------
    movie_scheme: MovieBaseSchema
        Pydantic model for movie creation
    movie_service: MovieCreateService
        Service for movie operations

    Returns
    -------
    movie: MovieCreateService
        Movie model

    """
    movie = await movie_service.create(movie_scheme)
    return movie


@movie_router.post(
    "/{movie_id}/review",
    summary="Add movie in watched for user.",
    status_code=status.HTTP_200_OK,
    response_model=ReviewCreateSchema,
)
async def add_movie_review(
    movie_id: int,
    review: ReviewBaseSchema = ReviewBaseSchema(),
    authorization: str = Header(...),
    review_service: ReviewService = Depends(get_review_service),
    user_service: UserService = Depends(get_user_service),
):
    """Review on movie.

    Parameters
    ----------
    movie_id: int
        Movie id
    review: ReviewBaseSchema
        User`s review on the given movie
    authorization: str
        Header 'authorization' with jwt token
    user_service: UserService
        Service for user operations
    review_service: ReviewService
        Service for review operations

    Returns
    -------
    review: ReviewCreateSchema
        Model of added review

    """
    user = await user_service.get_current_user(authorization)
    review = await review_service.create_review(movie_id, user.id, review)
    return review


@movie_router.get(
    "/{movie_id}/review",
    summary="Add movie in watched for user.",
    status_code=status.HTTP_200_OK,
    response_model=ReviewResponseSchema,
    response_model_exclude_none=True,  # is it necessary?
)
async def get_movie_review(
    movie_id: int,
    authorization: str = Header(...),
    review_service: ReviewService = Depends(get_review_service),
    user_service: UserService = Depends(get_user_service),
):
    """Review on movie.

    Parameters
    ----------
    movie_id: int
        Movie id
    authorization: str
        Header 'authorization' with jwt token
    user_service: UserService
        Service for user operations
    review_service: ReviewService
        Service for review operations

    Returns
    -------
    review: ReviewResponseSchema
        Review model

    """
    user = await user_service.get_current_user(authorization)
    review = await review_service.get_review(movie_id, user.id)
    return review


@movie_router.get(
    "/{movie_id}/reviews",
    summary="Get movie with reviews.",
    status_code=status.HTTP_200_OK,
    response_model=MovieReviewSchema,
    response_model_exclude_none=True,  # is it necessary?
)
async def get_movie_with_reviews(
    movie_id: int,
    movie_service: MovieService = Depends(get_movie_service),
):
    """Review on movie.

    Parameters
    ----------
    movie_id: int
        Movie id
    movie_service: MovieService
        Service for movie operations

    Returns
    -------
    movie: ReviewResponseSchema
        Review model

    """
    movie = await movie_service.get_movie_with_reviews(movie_id)
    return movie
