"""
Commission-related models
"""
from typing import List
from pydantic import BaseModel, Field
from .base import BaseResponse

class CommissionResponse(BaseModel):
    """Commission response model"""
    commissionId: int = Field(description="Commission ID")
    commissionNameEn: str = Field(description="Commission name in English")
    circuitAdditionBenchStatus: bool = Field(description="Circuit bench status")
    activeStatus: bool = Field(description="Active status")

class CommissionsResponse(BaseResponse):
    """Commissions list response model"""
    commissions: List[CommissionResponse] = Field(description="List of commissions")
