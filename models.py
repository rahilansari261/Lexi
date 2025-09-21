from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class StateResponse(BaseModel):
    id: str
    name: str

class CommissionResponse(BaseModel):
    id: str
    name: str

class CaseResponse(BaseModel):
    case_number: str
    case_stage: str
    filing_date: str
    complainant: str
    complainant_advocate: str
    respondent: str
    respondent_advocate: str
    document_link: str

class CaseSearchRequest(BaseModel):
    state: str
    commission: str
    search_value: str

class StateListResponse(BaseModel):
    states: List[StateResponse]

class CommissionListResponse(BaseModel):
    commissions: List[CommissionResponse]