from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.schemas.category import CategoryResponse


class JobCreate(BaseModel):
    title: str
    category_id: Optional[UUID] = None


class JobUpdate(BaseModel):
    title: Optional[str] = None
    category_id: Optional[UUID] = None


class JobResponse(BaseModel):
    id: UUID
    title: str
    category_id: Optional[UUID] = None
    category: Optional[CategoryResponse] = None

    model_config = ConfigDict(from_attributes=True)
