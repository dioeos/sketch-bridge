from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from src.config import config
from src.database import sessionmanager

from src.auth.router import router as user_router
from src.sockets.router import router as room_ws_router

from src.auth.exceptions import email_exists_exception_handler
from src.auth.exceptions import EmailAlreadyExists


origins = ["http://localhost", "http://localhost:8080", "http://localhost:5173"]


def init_app(init_db=True) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if init_db:
            sessionmanager.init(config.DB_CONFIG)
        try:
            yield
        finally:
            if init_db and sessionmanager._engine is not None:
                await sessionmanager.close()

    server = FastAPI(title="Sketch Bridge", lifespan=lifespan, version="0.1.0")
    # routers
    server.include_router(user_router, prefix="/api", tags=["user"])
    server.include_router(room_ws_router, tags=["room"])

    # exception handlers
    server.add_exception_handler(EmailAlreadyExists, email_exists_exception_handler)

    server.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return server


app = init_app()
