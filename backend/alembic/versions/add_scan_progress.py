"""add progress to scan

Revision ID: add_scan_progress
Revises: 00d9f9210494
Create Date: 2026-01-31

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_scan_progress'
down_revision = '00d9f9210494'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('scan', sa.Column('progress', sa.Integer(), nullable=True, server_default='0'))


def downgrade():
    op.drop_column('scan', 'progress')
