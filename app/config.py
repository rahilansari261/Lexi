"""
Application configuration settings
"""
import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # API Configuration
    API_TITLE: str = "Jagriti Case Search API"
    API_DESCRIPTION: str = "API for searching cases from Jagriti portal"
    API_VERSION: str = "1.0.0"
    API_DOCS_URL: str = "/docs"
    API_REDOC_URL: str = "/redoc"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Jagriti API Configuration
    JAGRITI_BASE_URL: str = "https://e-jagriti.gov.in"
    JAGRITI_TIMEOUT: float = 30.0
    
    # CORS Configuration
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    # Pagination Defaults
    DEFAULT_PAGE_SIZE: int = 30
    MAX_PAGE_SIZE: int = 100
    
    # Date Configuration
    DEFAULT_FROM_DATE: str = "2025-01-01"
    DEFAULT_TO_DATE: str = "2025-09-22"
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# Global settings instance
settings = Settings()
