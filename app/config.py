"""
Application configuration settings
"""
import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # API Configuration
    API_TITLE: str = "Jagriti States & Commissions API"
    API_DESCRIPTION: str = "API for fetching states and commissions from Jagriti portal"
    API_VERSION: str = "1.0.0"
    API_DOCS_URL: str = "/docs"
    API_REDOC_URL: str = "/redoc"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # PDF Storage Configuration
    PDF_STORAGE_DIR: str = "pdf_storage"
    PDF_CLEANUP_DAYS: int = int(os.getenv("PDF_CLEANUP_DAYS", "30"))
    
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
    
    def get_base_url(self) -> str:
        """Get the appropriate base URL for the environment"""
        # Check for explicit BASE_URL environment variable
        base_url = os.getenv("BASE_URL")
        if base_url:
            return base_url
        
        # Check if we're in production (Railway)
        if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PUBLIC_DOMAIN"):
            railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
            if railway_domain:
                return f"https://{railway_domain}"
            else:
                # Fallback to known Railway domain
                return "https://lexi-production-3bd4.up.railway.app"
        
        # Development environment
        if self.HOST == "0.0.0.0":
            return f"http://localhost:{self.PORT}"
        else:
            return f"http://{self.HOST}:{self.PORT}"
    
    @property
    def BASE_URL(self) -> str:
        """Get the base URL for the current environment"""
        return self.get_base_url()

# Global settings instance
settings = Settings()
