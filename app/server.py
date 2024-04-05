from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from app.container import Container
from app.user.adapter.input.api import router as user_router
from app.auth.adapter.input.api import router as auth_router
from core.exceptions import CustomException
from core.fastapi.middlewares import SQLAlchemyMiddleware, AuthenticationMiddleware, AuthBackend


def init_routers(app: FastAPI):
    container = Container()
    user_router.container = container
    auth_router.container = container
    app.include_router(user_router)
    app.include_router(auth_router)


def init_listeners(app: FastAPI):
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={
                "error": exc.error_code,
                "message": exc.message
            }
        )

def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )

def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=["*"],
            allow_methods=["*"],
            allow_headers=["*"]
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(SQLAlchemyMiddleware),
    ]
    return middleware


def create_app() -> FastAPI:
    app = FastAPI(
        title="Basic",
        version="1.0.0",
        middleware=make_middleware()
    )
    init_routers(app)
    init_listeners(app)
    return app


app = create_app()