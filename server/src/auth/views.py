from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.auth.models import User as UserModel
from src.auth.schemas import UserSchemaCreate, UserSchema

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/get-user", response_model=UserSchema)
async def get_user(id: str, db: AsyncSession = Depends(get_db)):
    user = await UserModel.get(db, id)
    return user


@router.get("/get-users", response_model=list[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await UserModel.get_all(db)
    return users


@router.post("/create-user", response_model=UserSchema)
async def create_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_db)):
    new_user = await UserModel.create(db, **user.model_dump())
    return new_user
