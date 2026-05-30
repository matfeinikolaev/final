import enum

from app.models.base import IsDeletedModel
from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class ResumeStatus(str, enum.Enum):
    NEW = "NEW"
    REVIEWING = "REVIEWING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class ResumeCategory(str, enum.Enum):
    DEV = "DEV"
    MANAGEMENT = "MANAGEMENT"
    SALES = "SALES"


class Resume(IsDeletedModel):
    __tablename__ = "resumes"

    applicant_name = Column(String(200), nullable=False)
    applicant_email = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    category = Column(SQLEnum(ResumeCategory), nullable=True)
    status = Column(SQLEnum(ResumeStatus), nullable=False, default=ResumeStatus.NEW)
    vacancy_id = Column(UUID(as_uuid=True), ForeignKey("vacancies.id", ondelete="SET NULL"), nullable=True)

    vacancy = relationship("Vacancy", lazy="selectin")

    def __repr__(self):
        return f"<Resume {self.applicant_name}>"
