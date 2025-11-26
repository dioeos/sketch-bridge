from fastapi import Request
from fastapi.responses import JSONResponse
from src.logger import logger


class EmailAlreadyExists(Exception):
    def __init__(self, email: str):
        self.email = email


async def email_exists_exception_handler(request: Request, exc: Exception):
    logger.exception("Handling email already exists...")
    assert isinstance(exc, EmailAlreadyExists)
    return JSONResponse(
        status_code=409, content={"message": f"{exc.email} already exists"}
    )
