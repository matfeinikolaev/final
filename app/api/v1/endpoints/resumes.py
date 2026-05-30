from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import deps
from app.core.database import get_db
from app.models.resume import Resume, ResumeCategory, ResumeStatus
from app.models.user import User
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeResponse

router = APIRouter()


@router.get("/", response_model=List[ResumeResponse])
async def get_resumes(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category: Optional[ResumeCategory] = None,
    status: Optional[ResumeStatus] = None,
    vacancy_id: Optional[UUID] = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    query = select(Resume).where(Resume.is_deleted == False)
    if category:
        query = query.where(Resume.category == category)
    if status:
        query = query.where(Resume.status == status)
    if vacancy_id:
        query = query.where(Resume.vacancy_id == vacancy_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    result = await db.execute(select(Resume).where(Resume.id == resume_id, Resume.is_deleted == False))
    resume = result.scalars().first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@router.post("/", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(
    resume_in: ResumeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    resume = Resume(**resume_in.model_dump())
    db.add(resume)
    await db.commit()
    await db.refresh(resume)
    return resume


@router.patch("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: UUID,
    resume_in: ResumeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    result = await db.execute(select(Resume).where(Resume.id == resume_id, Resume.is_deleted == False))
    resume = result.scalars().first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    for field, value in resume_in.model_dump(exclude_unset=True).items():
        setattr(resume, field, value)
    await db.commit()
    await db.refresh(resume)
    return resume


@router.delete("/{resume_id}", response_model=ResumeResponse)
async def delete_resume(
    resume_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    result = await db.execute(select(Resume).where(Resume.id == resume_id, Resume.is_deleted == False))
    resume = result.scalars().first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    resume.is_deleted = True
    await db.commit()
    return resume
