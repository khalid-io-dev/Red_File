from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class PayloadTypeEnum(str, enum.Enum):
    REVERSE_SHELL = "reverse_shell"
    TROJAN = "trojan"
    RAT = "rat"
    DLL_HIJACK = "dll_hijack"
    PROCESS_INJECTION = "process_injection"
    FILELESS = "fileless"

class PlatformEnum(str, enum.Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"
    ANDROID = "android"

class LanguageEnum(str, enum.Enum):
    PYTHON = "python"
    POWERSHELL = "powershell"
    BASH = "bash"
    C = "c"
    CPP = "cpp"
    CSHARP = "csharp"
    GO = "go"

class Payload(Base):
    __tablename__ = "payload"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    payload_type = Column(SQLEnum(PayloadTypeEnum), nullable=False)
    platform = Column(SQLEnum(PlatformEnum), nullable=False)
    language = Column(SQLEnum(LanguageEnum), nullable=False)
    
    code = Column(Text)
    obfuscated_code = Column(Text)
    file_path = Column(String(500))
    embedded_file_path = Column(String(500))
    
    lhost = Column(String(100))
    lport = Column(Integer)
    
    evasion_techniques = Column(JSON)
    detection_rate = Column(Float)
    tested_at = Column(DateTime)
    
    owner_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User")
