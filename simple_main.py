from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
from typing import Dict, List, Any

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

@app.get("/")
async def root():
    return {"message": "Jagriti Case Search API", "version": "1.0.0"}

@app.get("/states")
async def get_states():
    """Get all available states with their internal IDs"""
    # Mock data for demonstration - in production this would scrape from Jagriti
    states = [
        {"id": "1", "name": "KARNATAKA"},
        {"id": "2", "name": "MAHARASHTRA"},
        {"id": "3", "name": "TAMIL NADU"},
        {"id": "4", "name": "DELHI"},
        {"id": "5", "name": "WEST BENGAL"}
    ]
    return {"states": states}

@app.get("/commissions/{state_id}")
async def get_commissions(state_id: str):
    """Get all available commissions for a given state with their internal IDs"""
    # Mock data for demonstration - in production this would scrape from Jagriti
    commissions = [
        {"id": "1", "name": "Bangalore 1st & Rural Additional"},
        {"id": "2", "name": "Bangalore 2nd Additional"},
        {"id": "3", "name": "Mumbai 1st Additional"},
        {"id": "4", "name": "Chennai Additional"}
    ]
    return {"commissions": commissions}

@app.post("/cases/by-case-number")
async def search_by_case_number(request: Dict[str, Any]):
    """Search cases by case number"""
    return await search_cases("case_number", request)

@app.post("/cases/by-complainant")
async def search_by_complainant(request: Dict[str, Any]):
    """Search cases by complainant name"""
    return await search_cases("complainant", request)

@app.post("/cases/by-respondent")
async def search_by_respondent(request: Dict[str, Any]):
    """Search cases by respondent name"""
    return await search_cases("respondent", request)

@app.post("/cases/by-complainant-advocate")
async def search_by_complainant_advocate(request: Dict[str, Any]):
    """Search cases by complainant advocate name"""
    return await search_cases("complainant_advocate", request)

@app.post("/cases/by-respondent-advocate")
async def search_by_respondent_advocate(request: Dict[str, Any]):
    """Search cases by respondent advocate name"""
    return await search_cases("respondent_advocate", request)

@app.post("/cases/by-industry-type")
async def search_by_industry_type(request: Dict[str, Any]):
    """Search cases by industry type"""
    return await search_cases("industry_type", request)

@app.post("/cases/by-judge")
async def search_by_judge(request: Dict[str, Any]):
    """Search cases by judge name"""
    return await search_cases("judge", request)

async def search_cases(search_type: str, request: Dict[str, Any]):
    """Common search function for all case search endpoints"""
    try:
        state = request.get("state", "")
        commission = request.get("commission", "")
        search_value = request.get("search_value", "")
        
        # Validate required fields
        if not state or not commission or not search_value:
            raise HTTPException(status_code=400, detail="Missing required fields: state, commission, search_value")
        
        # Mock response for demonstration - in production this would scrape from Jagriti
        mock_cases = [
            {
                "case_number": "123/2025",
                "case_stage": "Hearing",
                "filing_date": "2025-02-01",
                "complainant": "John Doe",
                "complainant_advocate": "Adv. Reddy",
                "respondent": "XYZ Ltd.",
                "respondent_advocate": "Adv. Mehta",
                "document_link": "https://e-jagriti.gov.in/case/123/2025"
            },
            {
                "case_number": "456/2025",
                "case_stage": "Disposed",
                "filing_date": "2025-01-15",
                "complainant": "Jane Smith",
                "complainant_advocate": "Adv. Kumar",
                "respondent": "ABC Corp",
                "respondent_advocate": "Adv. Singh",
                "document_link": "https://e-jagriti.gov.in/case/456/2025"
            }
        ]
        
        # Filter based on search criteria (simplified for demo)
        filtered_cases = []
        for case in mock_cases:
            if search_value.lower() in case.get(search_type.replace("_", "_"), "").lower():
                filtered_cases.append(case)
        
        return filtered_cases
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)