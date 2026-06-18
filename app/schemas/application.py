from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    resume_id: UUID
    vacancy_id: UUID


class ApplicationResponse(BaseModel):
    id: UUID
    resume_id: Optional[UUID] = None
    vacancy_id: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)
