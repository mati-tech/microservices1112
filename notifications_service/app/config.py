
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "")
    
    # Email
    email_host: str = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    email_port: int = int(os.getenv("EMAIL_PORT", 587))
    email_user: str = os.getenv("EMAIL_USER", "")
    email_password: str = os.getenv("EMAIL_PASSWORD", "")
    email_from: str = os.getenv("EMAIL_FROM", "noreply@educenter.com")
    
    # Retry settings
    max_retry_attempts: int = 3
    retry_delay_seconds: int = 60
    
    class Config:
        env_file = ".env"

settings = Settings()