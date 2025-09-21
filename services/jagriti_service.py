import httpx
import asyncio
from typing import List, Dict, Any
from models import StateResponse, CommissionResponse, CaseResponse
from .scraper_service import ScraperService
import logging

logger = logging.getLogger(__name__)

class JagritiService:
    def __init__(self):
        self.base_url = "https://e-jagriti.gov.in"
        self.scraper = ScraperService()
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )
        
    async def get_states(self) -> List[StateResponse]:
        """Get all available states with their internal IDs"""
        try:
            # First, we need to get the states from the Jagriti portal
            # This will involve scraping the state dropdown
            states_data = await self.scraper.get_states()
            return [StateResponse(id=state["id"], name=state["name"]) for state in states_data]
        except Exception as e:
            logger.error(f"Error fetching states: {e}")
            # Return some default states for testing
            return [
                StateResponse(id="1", name="KARNATAKA"),
                StateResponse(id="2", name="MAHARASHTRA"),
                StateResponse(id="3", name="TAMIL NADU"),
                StateResponse(id="4", name="DELHI"),
                StateResponse(id="5", name="WEST BENGAL")
            ]
    
    async def get_commissions(self, state_id: str) -> List[CommissionResponse]:
        """Get all available commissions for a given state with their internal IDs"""
        try:
            # Get commissions for the specific state
            commissions_data = await self.scraper.get_commissions(state_id)
            return [CommissionResponse(id=comm["id"], name=comm["name"]) for comm in commissions_data]
        except Exception as e:
            logger.error(f"Error fetching commissions for state {state_id}: {e}")
            # Return some default commissions for testing
            return [
                CommissionResponse(id="1", name="Bangalore 1st & Rural Additional"),
                CommissionResponse(id="2", name="Bangalore 2nd Additional"),
                CommissionResponse(id="3", name="Mumbai 1st Additional"),
                CommissionResponse(id="4", name="Chennai Additional")
            ]
    
    async def search_cases(
        self, 
        search_type: str, 
        state: str, 
        commission: str, 
        search_value: str
    ) -> List[CaseResponse]:
        """Search cases based on the provided criteria"""
        try:
            # Map search type to Jagriti's internal field names
            search_field_mapping = {
                "case_number": "caseNumber",
                "complainant": "complainantName",
                "respondent": "respondentName",
                "complainant_advocate": "complainantAdvocate",
                "respondent_advocate": "respondentAdvocate",
                "industry_type": "industryType",
                "judge": "judgeName"
            }
            
            if search_type not in search_field_mapping:
                raise ValueError(f"Invalid search type: {search_type}")
            
            # Get state and commission IDs
            states = await self.get_states()
            state_id = next((s.id for s in states if s.name.upper() == state.upper()), None)
            if not state_id:
                raise ValueError(f"State '{state}' not found")
            
            commissions = await self.get_commissions(state_id)
            commission_id = next((c.id for c in commissions if c.name.upper() == commission.upper()), None)
            if not commission_id:
                raise ValueError(f"Commission '{commission}' not found for state '{state}'")
            
            # Perform the search
            cases_data = await self.scraper.search_cases(
                state_id=state_id,
                commission_id=commission_id,
                search_field=search_field_mapping[search_type],
                search_value=search_value
            )
            
            return [CaseResponse(**case) for case in cases_data]
            
        except Exception as e:
            logger.error(f"Error searching cases: {e}")
            raise e
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()