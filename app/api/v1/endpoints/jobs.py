from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import deps
from app.core.database import get_db
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate, JobUpdate, JobResponse

router = APIRouter()


@router.get("/", response_model=List[JobResponse])
async def get_jobs(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    result = await db.execute(select(Job).where(Job.is_deleted == False).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(Job).where(Job.id == job_id, Job.is_deleted == False))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_in: JobCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_superuser),
) -> Any:
    job = Job(title=job_in.title, category_id=job_in.category_id)
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: UUID,
    job_in: JobUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_superuser),
) -> Any:
    result = await db.execute(select(Job).where(Job.id == job_id, Job.is_deleted == False))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    for field, value in job_in.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    await db.commit()
    await db.refresh(job)
    return job


@router.delete("/{job_id}", response_model=JobResponse)
async def delete_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_superuser),
) -> Any:
    result = await db.execute(select(Job).where(Job.id == job_id, Job.is_deleted == False))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.is_deleted = True
    await db.commit()
    return job
