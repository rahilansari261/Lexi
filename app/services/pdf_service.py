import base64
import os
import logging
from pathlib import Path
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

class PDFService:
    """Service for handling PDF storage and retrieval"""
    
    def __init__(self, storage_dir: str = "pdf_storage"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        # Get base URL from environment or construct from settings
        base_url = os.getenv("BASE_URL")
        if not base_url:
            # Check if we're in production (Railway)
            if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PUBLIC_DOMAIN"):
                # Use Railway's public domain
                railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
                if railway_domain:
                    base_url = f"https://{railway_domain}"
                else:
                    # Fallback to Railway's default domain pattern
                    base_url = "https://lexi-production-3bd4.up.railway.app"
            else:
                # Development environment
                if settings.HOST == "0.0.0.0":
                    base_url = f"http://localhost:{settings.PORT}"
                else:
                    base_url = f"http://{settings.HOST}:{settings.PORT}"
        
        self.base_url = base_url
        logger.info(f"PDF Service initialized with base URL: {self.base_url}")
    
    def store_pdf(self, base64_data: str, case_number: str) -> str:
        """
        Store base64 PDF data and return download URL
        
        Args:
            base64_data: Base64 encoded PDF data from Jagriti
            case_number: Case number for filename generation
            
        Returns:
            str: Download URL for the stored PDF
        """
        try:
            # Decode base64 data
            pdf_bytes = base64.b64decode(base64_data)
            
            # Generate unique filename based on case number
            safe_case_number = case_number.replace("/", "_").replace(" ", "_")
            filename = f"case_{safe_case_number}.pdf"
            
            # Store file
            file_path = self.storage_dir / filename
            with open(file_path, "wb") as f:
                f.write(pdf_bytes)
            
            # Generate download URL
            download_url = f"{self.base_url}/cases/download/{filename}"
            
            logger.info(f"PDF stored for case {case_number}: {download_url}")
            return download_url
            
        except Exception as e:
            logger.error(f"Error storing PDF for case {case_number}: {e}")
            raise Exception(f"Failed to store PDF: {str(e)}")
    
    def get_pdf_path(self, filename: str) -> Optional[Path]:
        """Get file path for download"""
        file_path = self.storage_dir / filename
        return file_path if file_path.exists() else None
    
    def get_pdf_by_case_number(self, case_number: str) -> Optional[Path]:
        """Get PDF file path by case number"""
        safe_case_number = case_number.replace("/", "_").replace(" ", "_")
        filename = f"case_{safe_case_number}.pdf"
        return self.get_pdf_path(filename)
    
    def delete_pdf(self, filename: str) -> bool:
        """Delete PDF file"""
        try:
            file_path = self.storage_dir / filename
            if file_path.exists():
                file_path.unlink()
                logger.info(f"PDF deleted: {filename}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting PDF {filename}: {e}")
            return False
