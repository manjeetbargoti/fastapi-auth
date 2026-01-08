"""create users table

Revision ID: 3c39e3ab410f
Revises: 
Create Date: 2026-01-08 13:06:29.478835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '3c39e3ab410f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),

        sa.Column("first_name", sa.String(length=100), nullable=True),
        sa.Column("last_name", sa.String(length=100), nullable=True),

        sa.Column("email", sa.String(length=100), unique=True, nullable=False, index=True),
        sa.Column("password", sa.String(length=255), nullable=False),

        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.false(), index=True),
        sa.Column("is_verified", sa.Boolean, nullable=False, server_default=sa.false(), index=True),
        sa.Column("is_admin", sa.Boolean, nullable=False, server_default=sa.false()),

        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("token_version", sa.Integer, default='0', nullable=False),

        sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True)
    )


def downgrade() -> None:
    op.drop_table("users")
