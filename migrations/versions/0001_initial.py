"""Initial migration

Revision ID: 0001_initial
Revises:
Create Date: 2025-01-01 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="false", comment="Soft delete flag"),
        sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Timestamp when the record was deleted"),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, comment="Unique identifier for the record"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="Timestamp when the record was created"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, comment="Timestamp when the record was last updated"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "categories",
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="false", comment="Soft delete flag"),
        sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Timestamp when the record was deleted"),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, comment="Unique identifier for the record"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="Timestamp when the record was created"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, comment="Timestamp when the record was last updated"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_categories_id"), "categories", ["id"], unique=False)

    op.create_table(
        "jobs",
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="false", comment="Soft delete flag"),
        sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Timestamp when the record was deleted"),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, comment="Unique identifier for the record"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="Timestamp when the record was created"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, comment="Timestamp when the record was last updated"),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_jobs_id"), "jobs", ["id"], unique=False)

    op.create_table(
        "vacancies",
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=True),
        sa.Column("category", sa.Enum("DEV", "MANAGEMENT", "SALES", name="vacancycategory"), nullable=True),
        sa.Column("status", sa.Enum("OPEN", "CLOSED", name="vacancystatus"), nullable=False, server_default="OPEN"),
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="false", comment="Soft delete flag"),
        sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Timestamp when the record was deleted"),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, comment="Unique identifier for the record"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="Timestamp when the record was created"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, comment="Timestamp when the record was last updated"),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_vacancies_id"), "vacancies", ["id"], unique=False)

    op.create_table(
        "resumes",
        sa.Column("applicant_name", sa.String(length=200), nullable=False),
        sa.Column("applicant_email", sa.String(length=200), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.Enum("DEV", "MANAGEMENT", "SALES", name="resumecategory"), nullable=True),
        sa.Column("status", sa.Enum("NEW", "REVIEWING", "ACCEPTED", "REJECTED", name="resumestatus"), nullable=False, server_default="NEW"),
        sa.Column("vacancy_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="false", comment="Soft delete flag"),
        sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Timestamp when the record was deleted"),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, comment="Unique identifier for the record"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="Timestamp when the record was created"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, comment="Timestamp when the record was last updated"),
        sa.ForeignKeyConstraint(["vacancy_id"], ["vacancies.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_resumes_id"), "resumes", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_resumes_id"), table_name="resumes")
    op.drop_table("resumes")
    op.drop_index(op.f("ix_vacancies_id"), table_name="vacancies")
    op.drop_table("vacancies")
    op.drop_index(op.f("ix_jobs_id"), table_name="jobs")
    op.drop_table("jobs")
    op.drop_index(op.f("ix_categories_id"), table_name="categories")
    op.drop_table("categories")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS vacancycategory")
    op.execute("DROP TYPE IF EXISTS vacancystatus")
    op.execute("DROP TYPE IF EXISTS resumecategory")
    op.execute("DROP TYPE IF EXISTS resumestatus")
