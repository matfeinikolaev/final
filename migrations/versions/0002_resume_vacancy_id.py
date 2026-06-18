"""resumes job_id to vacancy_id

Revision ID: 0002_resume_vacancy_id
Revises: 0001_initial
Create Date: 2025-01-02 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op

revision: str = "0002_resume_vacancy_id"
down_revision: Union[str, Sequence[str], None] = "0001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
