from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    app_name: str = "Mnemosyne API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database Settings (for future use)
    database_url: Optional[str] = None
    
    # Security Settings (for future use)
    secret_key: Optional[str] = None
    access_token_expire_minutes: int = 30
    
    # CORS Settings
    allowed_origins: list = ["*"]  # Configure properly for production
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
