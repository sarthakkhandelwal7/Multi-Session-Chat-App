from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.datastructures import State
from src.db import Postgres, DatabaseAdapter
from src.core.settings import Settings
import logging
from datetime import datetime, timezone
from src.api import chat_router, user_router
from src.service import ChatService, UserService


class DBUtilsAppState(State):
    postgres: Postgres
    settings: Settings
    chat_service: ChatService
    user_service: UserService
    db: DatabaseAdapter


settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Initializing application with settings: %s", settings)
    app.state = DBUtilsAppState()
    app.state.settings = settings

    async with Postgres(settings) as pg:
        logging.info("Connecting to Postgres")
        app.state.postgres = pg
        app.state.db = app.state.postgres

        # Initialize services with db and settings
        app.state.chat_service = ChatService(db=app.state.db, settings=settings)
        app.state.user_service = UserService(db=app.state.db, settings=settings)

        logging.info("Application startup complete")

        app.state.started_at = datetime.now(timezone.utc)

        yield


app = FastAPI(lifespan=lifespan, root_path=settings.root_path)
app.include_router(chat_router)
app.include_router(user_router)
