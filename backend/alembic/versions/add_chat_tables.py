"""add chat tables

Revision ID: add_chat_tables
Revises: add_scan_progress
Create Date: 2026-01-31

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_chat_tables'
down_revision = 'add_scan_progress'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('chat_session',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('model_name', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_session_id'), 'chat_session', ['id'], unique=False)
    op.create_index(op.f('ix_chat_session_user_id'), 'chat_session', ['user_id'], unique=False)
    
    op.create_table('chat_message',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=True),
        sa.Column('role', sa.String(length=20), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('enhanced_prompt', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['chat_session.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_message_id'), 'chat_message', ['id'], unique=False)
    op.create_index(op.f('ix_chat_message_session_id'), 'chat_message', ['session_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_chat_message_session_id'), table_name='chat_message')
    op.drop_index(op.f('ix_chat_message_id'), table_name='chat_message')
    op.drop_table('chat_message')
    op.drop_index(op.f('ix_chat_session_user_id'), table_name='chat_session')
    op.drop_index(op.f('ix_chat_session_id'), table_name='chat_session')
    op.drop_table('chat_session')