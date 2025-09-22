#!/usr/bin/env python3
"""
Jagriti States & Commissions API
Clean implementation with Swagger documentation
"""

import asyncio
import logging
from typing import List, Dict, Any
from jagriti_client import JagritiClient
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Jagriti client
client = JagritiClient()

# Create FastAPI app with Swagger
app = FastAPI(
    title="Jagriti States & Commissions API",
    description="API for fetching states and commissions from Jagriti portal",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for response documentation
class StateResponse(BaseModel):
    commissionId: int
    commissionNameEn: str
    circuitAdditionBenchStatus: bool
    activeStatus: bool

class CommissionResponse(BaseModel):
    commissionId: int
    commissionNameEn: str
    circuitAdditionBenchStatus: bool
    activeStatus: bool

class StatesResponse(BaseModel):
    states: List[StateResponse]

class CommissionsResponse(BaseModel):
    commissions: List[CommissionResponse]

# Pydantic models for case search
class CaseSearchRequest(BaseModel):
    state: str
    commission: str
    search_value: str
    judge_id: str = ""  # Only for judge search
    page: int = 0
    size: int = 30
    from_date: str = "2025-01-01"
    to_date: str = "2025-09-22"

class CaseResponse(BaseModel):
    case_number: str
    case_stage: str
    filing_date: str
    complainant: str
    complainant_advocate: str
    respondent: str
    respondent_advocate: str
    document_link: str

class CaseSearchResponse(BaseModel):
    cases: List[CaseResponse]
    total_count: int
    page: int
    size: int

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Jagriti States & Commissions API", 
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/states", response_model=StatesResponse)
async def get_states():
    """
    Get all available states and union territories
    
    Returns a list of all states/UTs from the Jagriti portal with their commission IDs.
    Circuit benches and special benches are filtered out to show only main states.
    """
    try:
        states_data = await client.get_states()
        return {"states": states_data}
    except Exception as e:
        logger.error(f"Error fetching states: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch states: {str(e)}")

@app.get("/commissions/{state_id}", response_model=CommissionsResponse)
async def get_commissions(state_id: str):
    """
    Get all district commissions for a specific state
    
    - **state_id**: The commission ID of the state (e.g., 11290000 for Karnataka)
    
    Returns a list of all district commissions for the specified state.
    """
    try:
        commissions_data = await client.get_commissions(state_id)
        return {"commissions": commissions_data}
    except Exception as e:
        logger.error(f"Error fetching commissions for state {state_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch commissions: {str(e)}")

# Helper function to transform Jagriti case data to our format
def transform_case_data(case_data: Dict[str, Any]) -> CaseResponse:
    """Transform Jagriti case data to our standardized format"""
    return CaseResponse(
        case_number=case_data.get("caseNumber") or "",
        case_stage=case_data.get("caseStageName") or "",
        filing_date=case_data.get("caseFilingDate") or "",
        complainant=case_data.get("complainantName") or "",
        complainant_advocate=case_data.get("complainantAdvocateName") or "",
        respondent=case_data.get("respondentName") or "",
        respondent_advocate=case_data.get("respondentAdvocateName") or "",
        document_link=case_data.get("documentBase64") or ""
    )

# Case search endpoints
@app.post("/cases/by-case-number", response_model=CaseSearchResponse)
async def search_by_case_number(request: CaseSearchRequest):
    """Search cases by case number"""
    try:
        # Find state and commission IDs
        state_id = await client.find_state_id_by_name(request.state)
        commission_id = await client.find_commission_id_by_name(state_id, request.commission)
        print(f"**********************************")
        print(f"State ID: {state_id}, Commission ID: {commission_id}")
        print(f"**********************************")
        # Search cases
        result = await client.get_case_details_by_search(
            commission_id=commission_id,
            search_type=1,  # Case number search
            search_value=request.search_value,
            page=request.page,
            size=request.size,
            from_date=request.from_date,
            to_date=request.to_date
        )
        
        if result.get("status") == 200 and result.get("data"):
            cases = [transform_case_data(case) for case in result["data"]]
            return CaseSearchResponse(
                cases=cases,
                total_count=result.get("totalCount", len(cases)),
                page=request.page,
                size=request.size
            )
        else:
            return CaseSearchResponse(cases=[], total_count=0, page=request.page, size=request.size)
            
    except Exception as e:
        logger.error(f"Error in case number search: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/cases/by-complainant", response_model=CaseSearchResponse)
async def search_by_complainant(request: CaseSearchRequest):
    """Search cases by complainant name"""
    try:
        state_id = await client.find_state_id_by_name(request.state)
        commission_id = await client.find_commission_id_by_name(state_id, request.commission)
        
        result = await client.get_case_details_by_search(
            commission_id=commission_id,
            search_type=2,  # Complainant search
            search_value=request.search_value,
            page=request.page,
            size=request.size,
            from_date=request.from_date,
            to_date=request.to_date
        )
        
        if result.get("status") == 200 and result.get("data"):
            cases = [transform_case_data(case) for case in result["data"]]
            return CaseSearchResponse(
                cases=cases,
                total_count=result.get("totalCount", len(cases)),
                page=request.page,
                size=request.size
            )
        else:
            return CaseSearchResponse(cases=[], total_count=0, page=request.page, size=request.size)
            
    except Exception as e:
        logger.error(f"Error in complainant search: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/cases/by-respondent", response_model=CaseSearchResponse)
async def search_by_respondent(request: CaseSearchRequest):
    """Search cases by respondent name"""
    try:
        state_id = await client.find_state_id_by_name(request.state)
        commission_id = await client.find_commission_id_by_name(state_id, request.commission)
        
        result = await client.get_case_details_by_search(
            commission_id=commission_id,
            search_type=3,  # Respondent search
            search_value=request.search_value,
            page=request.page,
            size=request.size,
            from_date=request.from_date,
            to_date=request.to_date
        )
        
        if result.get("status") == 200 and result.get("data"):
            cases = [transform_case_data(case) for case in result["data"]]
            return CaseSearchResponse(
                cases=cases,
                total_count=result.get("totalCount", len(cases)),
                page=request.page,
                size=request.size
            )
        else:
            return CaseSearchResponse(cases=[], total_count=0, page=request.page, size=request.size)
            
    except Exception as e:
        logger.error(f"Error in respondent search: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/cases/by-complainant-advocate", response_model=CaseSearchResponse)
async def search_by_complainant_advocate(request: CaseSearchRequest):
    """Search cases by complainant advocate name"""
    try:
        state_id = await client.find_state_id_by_name(request.state)
        commission_id = await client.find_commission_id_by_name(state_id, request.commission)
        
        result = await client.get_case_details_by_search(
            commission_id=commission_id,
            search_type=4,  # Complainant advocate search
            search_value=request.search_value,
            page=request.page,
            size=request.size,
            from_date=request.from_date,
            to_date=request.to_date
        )
        
        if result.get("status") == 200 and result.get("data"):
            cases = [transform_case_data(case) for case in result["data"]]
            return CaseSearchResponse(
                cases=cases,
                total_count=result.get("totalCount", len(cases)),
                page=request.page,
                size=request.size
            )
        else:
            return CaseSearchResponse(cases=[], total_count=0, page=request.page, size=request.size)
            
    except Exception as e:
        logger.error(f"Error in complainant advocate search: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/cases/by-respondent-advocate", response_model=CaseSearchResponse)
async def search_by_respondent_advocate(request: CaseSearchRequest):
    """Search cases by respondent advocate name"""
    try:
        state_id = await client.find_state_id_by_name(request.state)
        commission_id = await client.find_commission_id_by_name(state_id, request.commission)
        
        result = await client.get_case_details_by_search(
            commission_id=commission_id,
            search_type=5,  # Respondent advocate search
            search_value=request.search_value,
            page=request.page,
            size=request.size,
            from_date=request.from_date,
            to_date=request.to_date
        )
        
        if result.get("status") == 200 and result.get("data"):
            cases = [transform_case_data(case) for case in result["data"]]
            return CaseSearchResponse(
                cases=cases,
                total_count=result.get("totalCount", len(cases)),
                page=request.page,
                size=request.size
            )
        else:
            return CaseSearchResponse(cases=[], total_count=0, page=request.page, size=request.size)
            
    except Exception as e:
        logger.error(f"Error in respondent advocate search: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/cases/by-industry-type", response_model=CaseSearchResponse)
async def search_by_industry_type(request: CaseSearchRequest):
    """Search cases by industry type"""
    try:
        state_id = await client.find_state_id_by_name(request.state)
        commission_id = await client.find_commission_id_by_name(state_id, request.commission)
        
        result = await client.get_case_details_by_search(
            commission_id=commission_id,
            search_type=6,  # Industry type search
            search_value=request.search_value,
            page=request.page,
            size=request.size,
            from_date=request.from_date,
            to_date=request.to_date
        )
        
        if result.get("status") == 200 and result.get("data"):
            cases = [transform_case_data(case) for case in result["data"]]
            return CaseSearchResponse(
                cases=cases,
                total_count=result.get("totalCount", len(cases)),
                page=request.page,
                size=request.size
            )
        else:
            return CaseSearchResponse(cases=[], total_count=0, page=request.page, size=request.size)
            
    except Exception as e:
        logger.error(f"Error in industry type search: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/cases/by-judge", response_model=CaseSearchResponse)
async def search_by_judge(request: CaseSearchRequest):
    """Search cases by judge"""
    try:
        state_id = await client.find_state_id_by_name(request.state)
        commission_id = await client.find_commission_id_by_name(state_id, request.commission)
        
        result = await client.get_case_details_by_search(
            commission_id=commission_id,
            search_type=7,  # Judge search
            search_value=request.search_value,
            judge_id=request.judge_id,
            page=request.page,
            size=request.size,
            from_date=request.from_date,
            to_date=request.to_date
        )
        
        if result.get("status") == 200 and result.get("data"):
            cases = [transform_case_data(case) for case in result["data"]]
            return CaseSearchResponse(
                cases=cases,
                total_count=result.get("totalCount", len(cases)),
                page=request.page,
                size=request.size
            )
        else:
            return CaseSearchResponse(cases=[], total_count=0, page=request.page, size=request.size)
            
    except Exception as e:
        logger.error(f"Error in judge search: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on app shutdown"""
    await client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
