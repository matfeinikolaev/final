from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.crud import crud_user

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_superuser),
) -> Any:
    result = await db.execute(select(User).where(User.is_deleted == False).offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_superuser),
) -> Any:
    existing = await crud_user.get_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    return await crud_user.create(db, obj_in=user_in)


@router.patch("/me", response_model=UserResponse)
async def update_me(
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    for field, value in user_in.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    await db.commit()
    await db.refresh(current_user)
    return current_user
