from .auth import auth_router
from .movie import movie_router
from .user import user_router

__all__ = [
    "auth_router",
    "user_router",
    "movie_router",
]
