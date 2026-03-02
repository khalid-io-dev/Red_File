"""create all tables

Revision ID: create_tables_001
Revises: 
Create Date: 2026-01-19

"""
from alembic import op
import sqlalchemy as sa


revision = 'create_tables_001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # User table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True, default=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_full_name'), 'user', ['full_name'], unique=False)

    # Scan table
    op.create_table(
        'scan',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('target_url', sa.String(500), nullable=False),
        sa.Column('scan_type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scan_id'), 'scan', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_scan_id'), table_name='scan')
    op.drop_table('scan')
    op.drop_index(op.f('ix_user_full_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
