"""Add findings, credentials, campaigns, reports tables

Revision ID: add_persistence_models
Revises: 
Create Date: 2024-01-27

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = 'add_persistence_models'
down_revision = 'create_tables_001'
branch_labels = None
depends_on = None

def upgrade():
    # Finding table
    op.create_table('finding',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('severity', sa.Enum('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO', name='severityenum'), nullable=True),
        sa.Column('status', sa.Enum('NEW', 'CONFIRMED', 'FALSE_POSITIVE', 'FIXED', 'IGNORED', name='statusenum'), nullable=True),
        sa.Column('target', sa.String(length=255), nullable=True),
        sa.Column('tool', sa.String(length=100), nullable=True),
        sa.Column('cve_id', sa.String(length=50), nullable=True),
        sa.Column('cvss_score', sa.String(length=10), nullable=True),
        sa.Column('evidence', sa.Text(), nullable=True),
        sa.Column('remediation', sa.Text(), nullable=True),
        sa.Column('references', sa.Text(), nullable=True),
        sa.Column('scan_id', sa.Integer(), nullable=True),
        sa.Column('campaign_id', sa.String(length=100), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['scan_id'], ['scan.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_finding_id'), 'finding', ['id'], unique=False)

    # Credential table
    op.create_table('credential',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=False),
        sa.Column('password', sa.Text(), nullable=False),
        sa.Column('hash_value', sa.Text(), nullable=True),
        sa.Column('service', sa.String(length=100), nullable=True),
        sa.Column('protocol', sa.String(length=50), nullable=True),
        sa.Column('port', sa.Integer(), nullable=True),
        sa.Column('target', sa.String(length=255), nullable=True),
        sa.Column('source_tool', sa.String(length=100), nullable=True),
        sa.Column('is_valid', sa.Boolean(), nullable=True),
        sa.Column('tested_at', sa.DateTime(), nullable=True),
        sa.Column('scan_id', sa.Integer(), nullable=True),
        sa.Column('campaign_id', sa.String(length=100), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['scan_id'], ['scan.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_credential_id'), 'credential', ['id'], unique=False)

    # Campaign table
    op.create_table('campaign',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('targets', sa.JSON(), nullable=True),
        sa.Column('chain_type', sa.String(length=50), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'RUNNING', 'PAUSED', 'COMPLETED', 'FAILED', name='campaignstatusenum'), nullable=True),
        sa.Column('progress', sa.Integer(), nullable=True),
        sa.Column('results', sa.JSON(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_campaign_id'), 'campaign', ['id'], unique=False)

    # Report table
    op.create_table('report',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('report_type', sa.Enum('EXECUTIVE', 'TECHNICAL', 'COMPLIANCE', name='reporttypeenum'), nullable=True),
        sa.Column('format', sa.Enum('JSON', 'MARKDOWN', 'PDF', 'HTML', name='reportformatenum'), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('file_path', sa.String(length=500), nullable=True),
        sa.Column('scan_id', sa.Integer(), nullable=True),
        sa.Column('campaign_id', sa.Integer(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['scan_id'], ['scan.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_report_id'), 'report', ['id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_report_id'), table_name='report')
    op.drop_table('report')
    op.drop_index(op.f('ix_campaign_id'), table_name='campaign')
    op.drop_table('campaign')
    op.drop_index(op.f('ix_credential_id'), table_name='credential')
    op.drop_table('credential')
    op.drop_index(op.f('ix_finding_id'), table_name='finding')
    op.drop_table('finding')
