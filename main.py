from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import (
    StateResponse, CommissionResponse, CaseResponse,
    CaseSearchRequest, StateListResponse, CommissionListResponse
)
from services.jagriti_service import JagritiService
from services.scraper_service import ScraperService
import uvicorn

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

# Initialize services
jagriti_service = JagritiService()
scraper_service = ScraperService()

@app.get("/")
async def root():
    return {"message": "Jagriti Case Search API", "version": "1.0.0"}

@app.get("/states", response_model=StateListResponse)
async def get_states():
    """Get all available states with their internal IDs"""
    try:
        states = await jagriti_service.get_states()
        return StateListResponse(states=states)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch states: {str(e)}")

@app.get("/commissions/{state_id}", response_model=CommissionListResponse)
async def get_commissions(state_id: str):
    """Get all available commissions for a given state with their internal IDs"""
    try:
        commissions = await jagriti_service.get_commissions(state_id)
        return CommissionListResponse(commissions=commissions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch commissions: {str(e)}")

@app.post("/cases/by-case-number", response_model=list[CaseResponse])
async def search_by_case_number(request: CaseSearchRequest):
    """Search cases by case number"""
    try:
        cases = await jagriti_service.search_cases(
            search_type="case_number",
            state=request.state,
            commission=request.commission,
            search_value=request.search_value
        )
        return cases
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/cases/by-complainant", response_model=list[CaseResponse])
async def search_by_complainant(request: CaseSearchRequest):
    """Search cases by complainant name"""
    try:
        cases = await jagriti_service.search_cases(
            search_type="complainant",
            state=request.state,
            commission=request.commission,
            search_value=request.search_value
        )
        return cases
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/cases/by-respondent", response_model=list[CaseResponse])
async def search_by_respondent(request: CaseSearchRequest):
    """Search cases by respondent name"""
    try:
        cases = await jagriti_service.search_cases(
            search_type="respondent",
            state=request.state,
            commission=request.commission,
            search_value=request.search_value
        )
        return cases
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/cases/by-complainant-advocate", response_model=list[CaseResponse])
async def search_by_complainant_advocate(request: CaseSearchRequest):
    """Search cases by complainant advocate name"""
    try:
        cases = await jagriti_service.search_cases(
            search_type="complainant_advocate",
            state=request.state,
            commission=request.commission,
            search_value=request.search_value
        )
        return cases
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/cases/by-respondent-advocate", response_model=list[CaseResponse])
async def search_by_respondent_advocate(request: CaseSearchRequest):
    """Search cases by respondent advocate name"""
    try:
        cases = await jagriti_service.search_cases(
            search_type="respondent_advocate",
            state=request.state,
            commission=request.commission,
            search_value=request.search_value
        )
        return cases
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/cases/by-industry-type", response_model=list[CaseResponse])
async def search_by_industry_type(request: CaseSearchRequest):
    """Search cases by industry type"""
    try:
        cases = await jagriti_service.search_cases(
            search_type="industry_type",
            state=request.state,
            commission=request.commission,
            search_value=request.search_value
        )
        return cases
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/cases/by-judge", response_model=list[CaseResponse])
async def search_by_judge(request: CaseSearchRequest):
    """Search cases by judge name"""
    try:
        cases = await jagriti_service.search_cases(
            search_type="judge",
            state=request.state,
            commission=request.commission,
            search_value=request.search_value
        )
        return cases
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)