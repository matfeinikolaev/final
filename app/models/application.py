import enum

from app.models.base import IsDeletedModel
from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Application(IsDeletedModel):
    __tablename__ = "applications"
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="SET NULL"), nullable=True)
    vacancy_id = Column(UUID(as_uuid=True), ForeignKey("vacancies.id", ondelete="SET NULL"), nullable=True)

    def __repr__(self):
        return f"<Application {self.applicant_name}>"
