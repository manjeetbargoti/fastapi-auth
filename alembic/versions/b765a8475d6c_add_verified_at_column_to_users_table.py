"""add verified_at column to users table

Revision ID: b765a8475d6c
Revises: 299b29d79040
Create Date: 2026-01-04 15:37:25.650746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b765a8475d6c'
down_revision: Union[str, Sequence[str], None] = '299b29d79040'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('verified_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'verified_at')
