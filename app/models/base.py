import uuid
from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, delete
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base


class BaseModel(Base):
    """Base model with uuid and time tracking fields."""

    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        index=True,
        comment="Unique identifier for the record",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Timestamp when the record was created",
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Timestamp when the record was last updated",
    )


class IsDeletedModel(BaseModel):
    """Base model with soft delete."""

    __abstract__ = True

    is_deleted = Column(
        Boolean, default=False, nullable=False, comment="Soft delete flag"
    )

    deleted_at = Column(
        DateTime, nullable=True, comment="Timestamp when the record was deleted"
    )

    def delete(self):
        """Soft delete the record."""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

    async def hard_delete_by_query(db: AsyncSession, model_id: uuid.UUID):
        """Hard delete using query."""
        stmt = delete(IsDeletedModel).where(IsDeletedModel.id == model_id)
        await db.execute(stmt)
        await db.commit()
