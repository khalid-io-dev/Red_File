"""add_user_role

Revision ID: 00d9f9210494
Revises: 45ab3695d0c3
Create Date: 2026-01-28 19:21:15.503150

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00d9f9210494'
down_revision: Union[str, None] = '45ab3695d0c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('role', sa.String(50), server_default='viewer', nullable=False))


def downgrade() -> None:
    op.drop_column('user', 'role')
