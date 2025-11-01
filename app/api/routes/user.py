from app.db.repository import UserRepository
from app.db.session import get_session, async_session_maker
from fastapi import APIRouter, Depends, HTTPException

from app import schemas

router = APIRouter()


def get_user_repo():
    return UserRepository(async_session_maker)


@router.post("", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, repo: UserRepository = Depends(get_user_repo)):
    return await repo.create(user)


@router.get("", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, repo: UserRepository = Depends(get_user_repo)):
    return await repo.list(skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.User)
async def read_user(id: int, repo: UserRepository = Depends(get_user_repo)):
    result = await repo.get(id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result
