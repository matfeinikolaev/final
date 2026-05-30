from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.models.vacancy import VacancyCategory, VacancyStatus
from app.schemas.job import JobResponse


class VacancyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[VacancyCategory] = None
    status: Optional[VacancyStatus] = VacancyStatus.OPEN
    job_id: Optional[UUID] = None


class VacancyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[VacancyCategory] = None
    status: Optional[VacancyStatus] = None
    job_id: Optional[UUID] = None


class VacancyResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    category: Optional[VacancyCategory] = None
    status: VacancyStatus
    job_id: Optional[UUID] = None
    job: Optional[JobResponse] = None

    model_config = ConfigDict(from_attributes=True)
