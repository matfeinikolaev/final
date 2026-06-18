from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.models.resume import ResumeCategory, ResumeStatus


class ResumeCreate(BaseModel):
    applicant_id: Optional[UUID] = None
    description: Optional[str] = None
    category: Optional[ResumeCategory] = None
    status: Optional[ResumeStatus] = ResumeStatus.NEW


class ResumeUpdate(BaseModel):
    applicant_id: Optional[UUID] = None
    description: Optional[str] = None
    category: Optional[ResumeCategory] = None
    status: Optional[ResumeStatus] = None


class ResumeResponse(BaseModel):
    id: UUID
    applicant_id: Optional[UUID] = None
    description: Optional[str] = None
    category: Optional[ResumeCategory] = None
    status: ResumeStatus

    model_config = ConfigDict(from_attributes=True)
