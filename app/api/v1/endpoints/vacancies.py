from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import deps
from app.core.database import get_db
from app.models.vacancy import Vacancy, VacancyCategory, VacancyStatus
from app.models.application import Application
from app.models.resume import Resume
from app.models.user import User
from app.schemas.vacancy import VacancyCreate, VacancyUpdate, VacancyResponse

router = APIRouter()


@router.get("/", response_model=List[VacancyResponse])
async def get_vacancies(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category: Optional[VacancyCategory] = None,
    status: Optional[VacancyStatus] = None,
    job_id: Optional[UUID] = None,
) -> Any:
    query = select(Vacancy).where(Vacancy.is_deleted == False)
    if category:
        query = query.where(Vacancy.category == category)
    if status:
        query = query.where(Vacancy.status == status)
    if job_id:
        query = query.where(Vacancy.job_id == job_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{vacancy_id}", response_model=VacancyResponse)
async def get_vacancy(vacancy_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(Vacancy).where(Vacancy.id == vacancy_id, Vacancy.is_deleted == False))
    vacancy = result.scalars().first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return vacancy


@router.get("/{vacancy_id}/stats")
async def get_vacancy_stats(
    vacancy_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    result = await db.execute(select(Vacancy).where(Vacancy.id == vacancy_id, Vacancy.is_deleted == False))
    vacancy = result.scalars().first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    apps_result = await db.execute(
        select(Application, Resume, User)
        .join(Resume, Resume.id == Application.resume_id, isouter=True)
        .join(User, User.id == Resume.applicant_id, isouter=True)
        .where(Application.vacancy_id == vacancy_id, Application.is_deleted == False)
    )
    rows = apps_result.all()

    applicants = [
        {
            "application_id": str(app.id),
            "resume_id": str(app.resume_id) if app.resume_id else None,
            "resume_status": resume.status if resume else None,
            "resume_category": resume.category if resume else None,
            "resume_description": resume.description if resume else None,
            "applicant_id": str(user.id) if user else None,
            "applicant_email": user.email if user else None,
            "applicant_name": user.full_name if user else None,
        }
        for app, resume, user in rows
    ]

    return {
        "vacancy_id": str(vacancy_id),
        "title": vacancy.title,
        "total_applications": len(applicants),
        "applicants": applicants,
    }


@router.post("/", response_model=VacancyResponse, status_code=status.HTTP_201_CREATED)
async def create_vacancy(
    vacancy_in: VacancyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_superuser),
) -> Any:
    vacancy = Vacancy(**vacancy_in.model_dump())
    db.add(vacancy)
    await db.commit()
    await db.refresh(vacancy)
    return vacancy


@router.patch("/{vacancy_id}", response_model=VacancyResponse)
async def update_vacancy(
    vacancy_id: UUID,
    vacancy_in: VacancyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_superuser),
) -> Any:
    result = await db.execute(select(Vacancy).where(Vacancy.id == vacancy_id, Vacancy.is_deleted == False))
    vacancy = result.scalars().first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    for field, value in vacancy_in.model_dump(exclude_unset=True).items():
        setattr(vacancy, field, value)
    await db.commit()
    await db.refresh(vacancy)
    return vacancy


@router.post("/{vacancy_id}/close", response_model=VacancyResponse)
async def close_vacancy(
    vacancy_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_superuser),
) -> Any:
    result = await db.execute(select(Vacancy).where(Vacancy.id == vacancy_id, Vacancy.is_deleted == False))
    vacancy = result.scalars().first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    vacancy.status = VacancyStatus.CLOSED
    await db.commit()
    await db.refresh(vacancy)
    return vacancy


@router.delete("/{vacancy_id}", response_model=VacancyResponse)
async def delete_vacancy(
    vacancy_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_superuser),
) -> Any:
    result = await db.execute(select(Vacancy).where(Vacancy.id == vacancy_id, Vacancy.is_deleted == False))
    vacancy = result.scalars().first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    vacancy.is_deleted = True
    await db.commit()
    return vacancy
