"""
State-related models
"""
from typing import List
from pydantic import BaseModel, Field
from .base import BaseResponse

class StateResponse(BaseModel):
    """State response model"""
    commissionId: int = Field(description="State commission ID")
    commissionNameEn: str = Field(description="State name in English")
    circuitAdditionBenchStatus: bool = Field(description="Circuit bench status")
    activeStatus: bool = Field(description="Active status")

class StatesResponse(BaseResponse):
    """States list response model"""
    states: List[StateResponse] = Field(description="List of states")
