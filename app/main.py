from contextlib import asynccontextmanager

from fastapi import FastAPI

# from app.database import create_all
from app.routers import auth_router, movie_router, user_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Define logic that should be executed when application starts up and shutting down."""
    print("Starting")
    # await create_all()
    yield
    print("Shutting down")


def init_routers(application: FastAPI) -> None:
    """Initialuze endpoints from whole application."""
    application.include_router(auth_router, prefix="/auth")
    application.include_router(user_router, prefix="/users")
    application.include_router(movie_router, prefix="/movies")


def create_app() -> FastAPI:
    """Create FastAPI application with several details."""
    _app = FastAPI(title="Online Cinema API", version="0.2.0", docs_url="/docs", redoc_url=None, lifespan=lifespan)
    # app.middleware("http")(db_connection)
    # app.middleware("http")(exception_handler)

    init_routers(application=_app)

    return _app


app = create_app()


@app.get("/")
async def root():
    """Test."""
    return {"message": "Hello World yo"}
