# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.scan import Scan  # noqa
from app.models.finding import Finding  # noqa
from app.models.credential import Credential  # noqa
from app.models.campaign import Campaign  # noqa
from app.models.report import Report  # noqa
from app.models.user_management import UserActivity, Team, TeamMember  # noqa
from app.models.compliance import ComplianceFramework, ComplianceControl, ComplianceMapping  # noqa
from app.models.payload import Payload  # noqa
from app.models.social_engineering import SECampaign  # noqa
from app.models.analysis import MalwareAnalysis  # noqa
from app.models.honeypot import HoneypotLog, HoneypotInstance  # noqa
