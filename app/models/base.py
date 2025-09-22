"""
Base models and common types
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class BaseResponse(BaseModel):
    """Base response model"""
    success: bool = True
    message: str = "Success"

class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(default=0, ge=0, description="Page number (0-based)")
    size: int = Field(default=30, ge=1, le=100, description="Number of items per page")

class DateRangeParams(BaseModel):
    """Date range parameters"""
    from_date: str = Field(default="2025-01-01", description="Start date (YYYY-MM-DD)")
    to_date: str = Field(default="2025-09-22", description="End date (YYYY-MM-DD)")

class SearchType:
    """Search type constants"""
    CASE_NUMBER = 1
    COMPLAINANT = 2
    RESPONDENT = 3
    COMPLAINANT_ADVOCATE = 4
    RESPONDENT_ADVOCATE = 5
    INDUSTRY_TYPE = 6
    JUDGE = 7

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
