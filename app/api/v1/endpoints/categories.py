from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import deps
from app.core.database import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    result = await db.execute(select(Category).where(Category.is_deleted == False).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(Category).where(Category.id == category_id, Category.is_deleted == False))
    category = result.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_superuser),
) -> Any:
    category = Category(name=category_in.name)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    category_in: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_superuser),
) -> Any:
    result = await db.execute(select(Category).where(Category.id == category_id, Category.is_deleted == False))
    category = result.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, value in category_in.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    await db.commit()
    await db.refresh(category)
    return category


@router.delete("/{category_id}", response_model=CategoryResponse)
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_superuser),
) -> Any:
    result = await db.execute(select(Category).where(Category.id == category_id, Category.is_deleted == False))
    category = result.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.is_deleted = True
    await db.commit()
    return category
