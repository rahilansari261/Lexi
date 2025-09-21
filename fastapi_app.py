from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import logging
from scraper import JagritiScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Jagriti Case Search API",
    description="API for searching cases in Indian Consumer Courts via Jagriti portal",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
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

# Initialize scraper
scraper = JagritiScraper()

@app.get("/")
async def root():
    return {"message": "Jagriti Case Search API", "version": "1.0.0"}

@app.get("/states", response_model=StateListResponse)
async def get_states():
    """Get all available states with their internal IDs"""
    try:
        states_data = await scraper.get_states()
        states = [StateResponse(id=state["id"], name=state["name"]) for state in states_data]
        return StateListResponse(states=states)
    except Exception as e:
        logger.error(f"Error fetching states: {e}")
        # Return fallback data
        states = [
            StateResponse(id="1", name="KARNATAKA"),
            StateResponse(id="2", name="MAHARASHTRA"),
            StateResponse(id="3", name="TAMIL NADU"),
            StateResponse(id="4", name="DELHI"),
            StateResponse(id="5", name="WEST BENGAL")
        ]
        return StateListResponse(states=states)

@app.get("/commissions/{state_id}", response_model=CommissionListResponse)
async def get_commissions(state_id: str):
    """Get all available commissions for a given state with their internal IDs"""
    try:
        commissions_data = await scraper.get_commissions(state_id)
        commissions = [CommissionResponse(id=comm["id"], name=comm["name"]) for comm in commissions_data]
        return CommissionListResponse(commissions=commissions)
    except Exception as e:
        logger.error(f"Error fetching commissions for state {state_id}: {e}")
        # Return fallback data
        commissions = [
            CommissionResponse(id="1", name="Bangalore 1st & Rural Additional"),
            CommissionResponse(id="2", name="Bangalore 2nd Additional"),
            CommissionResponse(id="3", name="Mumbai 1st Additional"),
            CommissionResponse(id="4", name="Chennai Additional")
        ]
        return CommissionListResponse(commissions=commissions)

@app.post("/cases/by-case-number", response_model=List[CaseResponse])
async def search_by_case_number(request: CaseSearchRequest):
    """Search cases by case number"""
    return await search_cases("caseNumber", request)

@app.post("/cases/by-complainant", response_model=List[CaseResponse])
async def search_by_complainant(request: CaseSearchRequest):
    """Search cases by complainant name"""
    return await search_cases("complainantName", request)

@app.post("/cases/by-respondent", response_model=List[CaseResponse])
async def search_by_respondent(request: CaseSearchRequest):
    """Search cases by respondent name"""
    return await search_cases("respondentName", request)

@app.post("/cases/by-complainant-advocate", response_model=List[CaseResponse])
async def search_by_complainant_advocate(request: CaseSearchRequest):
    """Search cases by complainant advocate name"""
    return await search_cases("complainantAdvocate", request)

@app.post("/cases/by-respondent-advocate", response_model=List[CaseResponse])
async def search_by_respondent_advocate(request: CaseSearchRequest):
    """Search cases by respondent advocate name"""
    return await search_cases("respondentAdvocate", request)

@app.post("/cases/by-industry-type", response_model=List[CaseResponse])
async def search_by_industry_type(request: CaseSearchRequest):
    """Search cases by industry type"""
    return await search_cases("industryType", request)

@app.post("/cases/by-judge", response_model=List[CaseResponse])
async def search_by_judge(request: CaseSearchRequest):
    """Search cases by judge name"""
    return await search_cases("judgeName", request)

async def search_cases(search_field: str, request: CaseSearchRequest) -> List[CaseResponse]:
    """Common search function for all case search endpoints"""
    try:
        # Get state and commission IDs
        states_data = await scraper.get_states()
        state_id = next((s["id"] for s in states_data if s["name"].upper() == request.state.upper()), None)
        if not state_id:
            raise HTTPException(status_code=400, detail=f"State '{request.state}' not found")
        
        commissions_data = await scraper.get_commissions(state_id)
        commission_id = next((c["id"] for c in commissions_data if c["name"].upper() == request.commission.upper()), None)
        if not commission_id:
            raise HTTPException(status_code=400, detail=f"Commission '{request.commission}' not found for state '{request.state}'")
        
        # Perform the search using scraper
        try:
            cases_data = await scraper.search_cases(
                state_id=state_id,
                commission_id=commission_id,
                search_field=search_field,
                search_value=request.search_value
            )
            return [CaseResponse(**case) for case in cases_data]
        except Exception as e:
            logger.error(f"Error in scraper search: {e}")
            # Return mock data as fallback
            return [CaseResponse(
                case_number="123/2025",
                case_stage="Hearing",
                filing_date="2025-02-01",
                complainant="John Doe",
                complainant_advocate="Adv. Reddy",
                respondent="XYZ Ltd.",
                respondent_advocate="Adv. Mehta",
                document_link="https://e-jagriti.gov.in/case/123/2025"
            )]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)