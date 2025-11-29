from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from src.auth.utils import hash_password, get_psql_exception_code
from src.auth.exceptions import EmailAlreadyExists
from src.logger import logger


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    is_verified: Mapped[bool] = mapped_column(nullable=False)

    @classmethod
    async def create(cls, db: AsyncSession, id=None, **kwargs):
        if not id:
            id = uuid4().hex

        if "password" in kwargs:
            kwargs["password"] = hash_password(kwargs["password"])

        user = cls(id=id, is_verified=False, **kwargs)
        db.add(user)

        try:
            await db.commit()
        except IntegrityError as ie:
            await db.rollback()

            err_code = get_psql_exception_code(ie)
            if err_code == "23505":
                email: str = kwargs["email"]
                if email is None:
                    raise

                existing: str = await db.scalar(select(cls).where(cls.email == email))

                if existing is None:
                    raise

                if getattr(existing, "is_verified", False):
                    raise EmailAlreadyExists(email) from ie

                # returns if not verified, update fields
                logger.info("User not yet verified, updating fields...")
                return await cls.update(db, existing, **kwargs)

        except Exception as e:
            logger.exception(f"Unhandled error: {e}")
            raise

        else:
            await db.refresh(user)
            return user

    @classmethod
    async def get(cls, db: AsyncSession, id: str):
        try:
            transaction = await db.get(cls, id)
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def get_all(cls, db: AsyncSession):
        return (await db.execute(select(cls))).scalars().all()

    @classmethod
    async def update(cls, db: AsyncSession, user, **fields):
        for key, value in fields.items():
            setattr(user, key, value)

        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        await db.refresh(user)
        return user
