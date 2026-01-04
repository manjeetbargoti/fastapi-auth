"""add is_verified to users

Revision ID: 299b29d79040
Revises: 7453390f68cf
Create Date: 2026-01-03 22:28:59.422780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '299b29d79040'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=True, server_default=sa.sql.expression.false()))


def downgrade() -> None:
    op.drop_column('users', 'is_verified')