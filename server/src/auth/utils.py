from passlib.context import CryptContext
from sqlalchemy.exc import DBAPIError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def get_psql_exception_code(exc: DBAPIError) -> str:
    return getattr(exc.orig, "sqlstate", "")
