from types import FrameType
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from app.admin import setup_admin
from app.api.routes import api_router
from app.core.config import settings
from app.services.storage import initialize_storage
from app.db.session import engine, sync_engine


def setup_middleware(app: FastAPI):
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_static(app: FastAPI):
    app.mount(settings.STATIC_URL, StaticFiles(directory=settings.STATIC_DIR), name="static")
    app.mount(settings.STORAGE_URL, StaticFiles(directory=settings.STORAGE_DIR), name="uploads")


def start_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}}
    )
    app.debug = settings.DEBUG

    app.include_router(api_router)
    setup_static(app)
    setup_middleware(app)
    setup_admin(app)
    initialize_storage()

    @app.on_event("startup")
    async def startup_db_event():
        print("Database connection pool initialized.")

    @app.on_event("shutdown")
    async def shutdown_db_event():
        await engine.dispose()
        sync_engine.dispose()
        print("Database connection pool disposed.")

    return app


app = start_app()
