from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.models.resume import ResumeCategory, ResumeStatus
from app.schemas.vacancy import VacancyResponse


class ResumeCreate(BaseModel):
    applicant_name: str
    applicant_email: Optional[str] = None
    description: Optional[str] = None
    category: Optional[ResumeCategory] = None
    status: Optional[ResumeStatus] = ResumeStatus.NEW
    vacancy_id: Optional[UUID] = None


class ResumeUpdate(BaseModel):
    applicant_name: Optional[str] = None
    applicant_email: Optional[str] = None
    description: Optional[str] = None
    category: Optional[ResumeCategory] = None
    status: Optional[ResumeStatus] = None
    vacancy_id: Optional[UUID] = None


class ResumeResponse(BaseModel):
    id: UUID
    applicant_name: str
    applicant_email: Optional[str] = None
    description: Optional[str] = None
    category: Optional[ResumeCategory] = None
    status: ResumeStatus
    vacancy_id: Optional[UUID] = None
    vacancy: Optional[VacancyResponse] = None

    model_config = ConfigDict(from_attributes=True)
