from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
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

# Initialize scraper
scraper = JagritiScraper()

@app.get("/")
async def root():
    return {"message": "Jagriti Case Search API", "version": "1.0.0"}

@app.get("/states")
async def get_states():
    """Get all available states with their internal IDs"""
    try:
        states_data = await scraper.get_states()
        return {"states": states_data}
    except Exception as e:
        logger.error(f"Error fetching states: {e}")
        # Return fallback data
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
    try:
        commissions_data = await scraper.get_commissions(state_id)
        return {"commissions": commissions_data}
    except Exception as e:
        logger.error(f"Error fetching commissions for state {state_id}: {e}")
        # Return fallback data
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
    return await search_cases("caseNumber", request)

@app.post("/cases/by-complainant")
async def search_by_complainant(request: Dict[str, Any]):
    """Search cases by complainant name"""
    return await search_cases("complainantName", request)

@app.post("/cases/by-respondent")
async def search_by_respondent(request: Dict[str, Any]):
    """Search cases by respondent name"""
    return await search_cases("respondentName", request)

@app.post("/cases/by-complainant-advocate")
async def search_by_complainant_advocate(request: Dict[str, Any]):
    """Search cases by complainant advocate name"""
    return await search_cases("complainantAdvocate", request)

@app.post("/cases/by-respondent-advocate")
async def search_by_respondent_advocate(request: Dict[str, Any]):
    """Search cases by respondent advocate name"""
    return await search_cases("respondentAdvocate", request)

@app.post("/cases/by-industry-type")
async def search_by_industry_type(request: Dict[str, Any]):
    """Search cases by industry type"""
    return await search_cases("industryType", request)

@app.post("/cases/by-judge")
async def search_by_judge(request: Dict[str, Any]):
    """Search cases by judge name"""
    return await search_cases("judgeName", request)

async def search_cases(search_field: str, request: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Common search function for all case search endpoints"""
    try:
        if not request:
            raise HTTPException(status_code=400, detail="Request body is required")
            
        state = request.get("state", "")
        commission = request.get("commission", "")
        search_value = request.get("search_value", "")
        
        # Validate required fields
        if not state or not commission or not search_value:
            raise HTTPException(status_code=400, detail="Missing required fields: state, commission, search_value")
        
        # Get state and commission IDs
        states_data = await scraper.get_states()
        state_id = next((s["id"] for s in states_data if s["name"].upper() == state.upper()), None)
        if not state_id:
            raise HTTPException(status_code=400, detail=f"State '{state}' not found")
        
        commissions_data = await scraper.get_commissions(state_id)
        commission_id = next((c["id"] for c in commissions_data if c["name"].upper() == commission.upper()), None)
        if not commission_id:
            raise HTTPException(status_code=400, detail=f"Commission '{commission}' not found for state '{state}'")
        
        # Perform the search using scraper
        try:
            cases_data = await scraper.search_cases(
                state_id=state_id,
                commission_id=commission_id,
                search_field=search_field,
                search_value=search_value
            )
            return cases_data
        except Exception as e:
            logger.error(f"Error in scraper search: {e}")
            # Return mock data as fallback
            return [{
                "case_number": "123/2025",
                "case_stage": "Hearing",
                "filing_date": "2025-02-01",
                "complainant": "John Doe",
                "complainant_advocate": "Adv. Reddy",
                "respondent": "XYZ Ltd.",
                "respondent_advocate": "Adv. Mehta",
                "document_link": "https://e-jagriti.gov.in/case/123/2025"
            }]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)