"""add token_version column to users

Revision ID: 9cf8f5d111f2
Revises: b765a8475d6c
Create Date: 2026-01-05 10:13:18.094278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cf8f5d111f2'
down_revision: Union[str, Sequence[str], None] = 'b765a8475d6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('token_version', sa.Integer(), server_default='0'))


def downgrade() -> None:
    op.drop_column('users', 'token_version')
