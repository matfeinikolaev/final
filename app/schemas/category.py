from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: Optional[str] = None


class CategoryResponse(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)
