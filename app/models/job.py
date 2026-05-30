from app.models.base import IsDeletedModel
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Job(IsDeletedModel):
    __tablename__ = "jobs"

    title = Column(String(200), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    category = relationship("Category", lazy="selectin")

    def __repr__(self):
        return f"<Job {self.title}>"
