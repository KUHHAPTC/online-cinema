from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_all
from app.models.user import User
from app.routers import auth_router

# import database


@asynccontextmanager
async def lifespan(application: FastAPI):
    print("Starting")
    # await create_all()
    yield
    print("Shutting down")


def init_routers(application: FastAPI):
    application.include_router(auth_router, prefix="/auth")


def create_app() -> FastAPI:
    fastapi_app = FastAPI(
        title="Online Cinema API", version="0.1.0", docs_url="/docs", redoc_url=None, lifespan=lifespan
    )
    # app.middleware("http")(db_connection)
    # app.middleware("http")(exception_handler)

    init_routers(application=fastapi_app)

    return fastapi_app


app = create_app()


@app.get("/")
async def root():
    """Test."""
    return {"message": "Hello World yo"}


# @app.post("/signup", summary="User signup.", status_code=status.HTTP_200_OK, response_model=UserResponseModel)
# async def create_user(user: UserCreateModel, db_session=Depends(get_db)):
#     # validate_user_is_not_exist(cursor, user.email)
#     # user_id = insert_user(db, user)
#     print(user.dict())
#     new_user = User(**user.dict())
#     await new_user.save(db_session)
#     return new_user
