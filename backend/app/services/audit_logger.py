from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from app.db.base_class import Base

class AuditLog(Base):
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(String(100))
    changes = Column(JSON)
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    status = Column(String(20))
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class AuditLogger:
    def __init__(self, db):
        self.db = db
    
    async def log(
        self,
        user_id: int,
        action: str,
        resource_type: str = None,
        resource_id: str = None,
        changes: dict = None,
        status: str = "success",
        error: str = None
    ):
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            changes=changes,
            status=status,
            error_message=error
        )
        self.db.add(log)
        await self.db.commit()
    
    async def log_login(self, user_id: int, success: bool):
        await self.log(
            user_id=user_id,
            action="user.login",
            status="success" if success else "failed"
        )
    
    async def log_scan_created(self, user_id: int, scan_id: int):
        await self.log(
            user_id=user_id,
            action="scan.created",
            resource_type="scan",
            resource_id=str(scan_id)
        )
    
    async def log_finding_created(self, user_id: int, finding_id: int):
        await self.log(
            user_id=user_id,
            action="finding.created",
            resource_type="finding",
            resource_id=str(finding_id)
        )
    
    async def log_report_generated(self, user_id: int, report_id: int):
        await self.log(
            user_id=user_id,
            action="report.generated",
            resource_type="report",
            resource_id=str(report_id)
        )
