from sqlalchemy import Column, Integer, String, Text, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class ComplianceFramework(Base):
    __tablename__ = "compliance_framework"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    version = Column(String(50))
    description = Column(Text)
    controls = relationship("ComplianceControl", back_populates="framework")

class ComplianceControl(Base):
    __tablename__ = "compliance_control"
    
    id = Column(Integer, primary_key=True, index=True)
    framework_id = Column(Integer, ForeignKey("compliance_framework.id"))
    control_id = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    
    framework = relationship("ComplianceFramework", back_populates="controls")
    mappings = relationship("ComplianceMapping", back_populates="control")

class ComplianceMapping(Base):
    __tablename__ = "compliance_mapping"
    
    id = Column(Integer, primary_key=True, index=True)
    control_id = Column(Integer, ForeignKey("compliance_control.id"))
    finding_id = Column(Integer, ForeignKey("finding.id"))
    status = Column(String(50))
    evidence = Column(Text)
    notes = Column(Text)
    
    control = relationship("ComplianceControl", back_populates="mappings")

# Seed data for OWASP Top 10
OWASP_TOP_10 = {
    "name": "OWASP Top 10",
    "version": "2021",
    "controls": [
        {"control_id": "A01", "title": "Broken Access Control", "category": "Access Control"},
        {"control_id": "A02", "title": "Cryptographic Failures", "category": "Cryptography"},
        {"control_id": "A03", "title": "Injection", "category": "Input Validation"},
        {"control_id": "A04", "title": "Insecure Design", "category": "Design"},
        {"control_id": "A05", "title": "Security Misconfiguration", "category": "Configuration"},
        {"control_id": "A06", "title": "Vulnerable Components", "category": "Dependencies"},
        {"control_id": "A07", "title": "Authentication Failures", "category": "Authentication"},
        {"control_id": "A08", "title": "Software and Data Integrity Failures", "category": "Integrity"},
        {"control_id": "A09", "title": "Security Logging Failures", "category": "Logging"},
        {"control_id": "A10", "title": "Server-Side Request Forgery", "category": "SSRF"}
    ]
}
