import enum

from app.models.base import IsDeletedModel
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class VacancyStatus(str, enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class VacancyCategory(str, enum.Enum):
    DEV = "DEV"
    MANAGEMENT = "MANAGEMENT"
    SALES = "SALES"


class Vacancy(IsDeletedModel):
    __tablename__ = "vacancies"

    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    category = Column(SQLEnum(VacancyCategory), nullable=True)
    status = Column(SQLEnum(VacancyStatus), nullable=False, default=VacancyStatus.OPEN)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)

    job = relationship("Job", lazy="selectin")

    def __repr__(self):
        return f"<Vacancy {self.title}>"
