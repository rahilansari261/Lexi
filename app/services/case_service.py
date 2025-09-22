"""
Case service for handling case-related business logic
"""
import logging
from typing import List, Dict, Any
from app.models.case import CaseSearchRequest, CaseResponse, CaseSearchResponse
from app.models.base import SearchType
from app.services.jagriti_client import JagritiClient
from app.utils.exceptions import CaseSearchException
from app.utils.helpers import transform_case_data

logger = logging.getLogger(__name__)

class CaseService:
    """Service for handling case operations"""
    
    def __init__(self, jagriti_client: JagritiClient):
        self.jagriti_client = jagriti_client
    
    async def search_cases(
        self, 
        request: CaseSearchRequest, 
        search_type: int
    ) -> CaseSearchResponse:
        """
        Search cases by the specified search type
        
        Args:
            request: Case search request
            search_type: Type of search (SearchType enum)
            
        Returns:
            Case search response with results
        """
        try:
            # Find state and commission IDs
            state_id = await self.jagriti_client.find_state_id_by_name(request.state)
            commission_id = await self.jagriti_client.find_commission_id_by_name(
                state_id, request.commission
            )
            
            logger.info(f"Searching cases - State ID: {state_id}, Commission ID: {commission_id}")
            
            # Search cases
            result = await self.jagriti_client.get_case_details_by_search(
                commission_id=commission_id,
                search_type=search_type,
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
                    cases=[CaseResponse(**case) for case in cases],
                    total_count=result.get("totalCount", len(cases)),
                    page=request.page,
                    size=request.size
                )
            else:
                return CaseSearchResponse(
                    cases=[],
                    total_count=0,
                    page=request.page,
                    size=request.size
                )
                
        except Exception as e:
            logger.error(f"Error in case search: {e}")
            raise CaseSearchException(f"Case search failed: {str(e)}")
    
    async def search_by_case_number(self, request: CaseSearchRequest) -> CaseSearchResponse:
        """Search cases by case number"""
        return await self.search_cases(request, SearchType.CASE_NUMBER)
    
    async def search_by_complainant(self, request: CaseSearchRequest) -> CaseSearchResponse:
        """Search cases by complainant name"""
        return await self.search_cases(request, SearchType.COMPLAINANT)
    
    async def search_by_respondent(self, request: CaseSearchRequest) -> CaseSearchResponse:
        """Search cases by respondent name"""
        return await self.search_cases(request, SearchType.RESPONDENT)
    
    async def search_by_complainant_advocate(self, request: CaseSearchRequest) -> CaseSearchResponse:
        """Search cases by complainant advocate name"""
        return await self.search_cases(request, SearchType.COMPLAINANT_ADVOCATE)
    
    async def search_by_respondent_advocate(self, request: CaseSearchRequest) -> CaseSearchResponse:
        """Search cases by respondent advocate name"""
        return await self.search_cases(request, SearchType.RESPONDENT_ADVOCATE)
    
    async def search_by_industry_type(self, request: CaseSearchRequest) -> CaseSearchResponse:
        """Search cases by industry type"""
        return await self.search_cases(request, SearchType.INDUSTRY_TYPE)
    
    async def search_by_judge(self, request: CaseSearchRequest) -> CaseSearchResponse:
        """Search cases by judge"""
        return await self.search_cases(request, SearchType.JUDGE)
