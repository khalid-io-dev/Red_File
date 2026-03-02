from typing import Any, Dict, List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "SecureSight"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "YOUR_SECURE_SECRET_KEY"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # DATABASE
    # Use MySQL DSN format
    DATABASE_URL: str = "mysql+aiomysql://root:@localhost:3306/securesight"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # KAFKA
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    
    # Kali Linux SSH
    KALI_SSH_HOST: str = "192.168.56.101"
    KALI_SSH_PORT: int = 22
    KALI_SSH_USER: str = "hollow"
    KALI_SSH_PASS: str = ""
    KALI_SSH_KEY: str = ""
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"

settings = Settings()
