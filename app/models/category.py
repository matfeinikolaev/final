from app.models.base import IsDeletedModel
from sqlalchemy import Column, String


class Category(IsDeletedModel):
    __tablename__ = "categories"

    name = Column(String(200), nullable=False)

    def __repr__(self):
        return f"<Category {self.name}>"
