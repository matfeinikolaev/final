from app.models.base import IsDeletedModel
from sqlalchemy import Boolean, Column, String


class User(IsDeletedModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    @property
    def full_name(self) -> str:
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    def __repr__(self):
        return f"<User {self.email}>"
