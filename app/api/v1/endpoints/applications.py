from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import deps
from app.core.database import get_db
from app.models.application import Application
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationResponse

router = APIRouter()


@router.get("/", response_model=List[ApplicationResponse])
async def get_applications(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    vacancy_id: Optional[UUID] = None,
    resume_id: Optional[UUID] = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    query = select(Application).where(Application.is_deleted == False)
    if vacancy_id:
        query = query.where(Application.vacancy_id == vacancy_id)
    if resume_id:
        query = query.where(Application.resume_id == resume_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    result = await db.execute(
        select(Application).where(Application.id == application_id, Application.is_deleted == False)
    )
    application = result.scalars().first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    application_in: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    application = Application(**application_in.model_dump())
    db.add(application)
    await db.commit()
    await db.refresh(application)
    return application


@router.delete("/{application_id}", response_model=ApplicationResponse)
async def delete_application(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    result = await db.execute(
        select(Application).where(Application.id == application_id, Application.is_deleted == False)
    )
    application = result.scalars().first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    application.is_deleted = True
    await db.commit()
    return application
