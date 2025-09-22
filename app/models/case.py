"""
Case-related models
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from .base import BaseResponse, PaginationParams, DateRangeParams, SearchType

class CaseSearchRequest(BaseModel):
    """Case search request model"""
    state: str = Field(description="State name (e.g., 'KARNATAKA')")
    commission: str = Field(description="Commission name (e.g., 'Bangalore 1st & Rural Additional')")
    search_value: str = Field(description="Search value")
    judge_id: str = Field(default="", description="Judge ID (only for judge search)")
    page: int = Field(default=0, ge=0, description="Page number (0-based)")
    size: int = Field(default=30, ge=1, le=100, description="Number of results per page")
    from_date: str = Field(default="2025-01-01", description="Start date (YYYY-MM-DD)")
    to_date: str = Field(default="2025-09-22", description="End date (YYYY-MM-DD)")

class CaseResponse(BaseModel):
    """Case response model"""
    case_number: str = Field(description="Case number")
    case_stage: str = Field(description="Case stage")
    filing_date: str = Field(description="Filing date")
    complainant: str = Field(description="Complainant name")
    complainant_advocate: str = Field(description="Complainant advocate name")
    respondent: str = Field(description="Respondent name")
    respondent_advocate: str = Field(description="Respondent advocate name")
    document_link: str = Field(description="Document link")

class CaseSearchResponse(BaseResponse):
    """Case search response model"""
    cases: List[CaseResponse] = Field(description="List of cases")
    total_count: int = Field(description="Total number of cases")
    page: int = Field(description="Current page number")
    size: int = Field(description="Number of results per page")
