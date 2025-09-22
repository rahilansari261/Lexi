"""
Case service for handling case-related business logic
"""
import logging
from typing import List, Dict, Any
from app.models.case import CaseSearchRequest, CaseResponse, CaseSearchResponse
from app.models.base import SearchType
from app.services.jagriti_client import JagritiClient
from app.services.pdf_service import PDFService
from app.utils.exceptions import CaseSearchException
from app.utils.helpers import transform_case_data

logger = logging.getLogger(__name__)

class CaseService:
    """Service for handling case operations"""
    
    def __init__(self, jagriti_client: JagritiClient):
        self.jagriti_client = jagriti_client
        self.pdf_service = PDFService()  # Add PDF service
    
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
                cases = []
                for case_data in result["data"]:
                    # Log the case data to see what fields are available
                    logger.info(f"Case data fields: {list(case_data.keys())}")
                    
                    # Transform case data
                    transformed_case = transform_case_data(case_data)
                    
                    # Check if we have base64 PDF data from Jagriti
                    base64_pdf_data = case_data.get("documentBase64")  # From Jagriti response
                    
                    if base64_pdf_data:
                        logger.info(f"Found base64 PDF data for case {transformed_case['case_number']}")
                        # Store PDF and get download URL
                        try:
                            document_link = self.pdf_service.store_pdf(base64_pdf_data, transformed_case['case_number'])
                            logger.info(f"PDF stored successfully, download URL: {document_link}")
                        except Exception as e:
                            logger.warning(f"Failed to store PDF for case {transformed_case['case_number']}: {e}")
                            document_link = transformed_case.get('document_link', 'https://e-jagriti.gov.in/.../case123')
                    else:
                        logger.info(f"No base64 PDF data found for case {transformed_case['case_number']}")
                        # Use original document link
                        document_link = transformed_case.get('document_link', 'https://e-jagriti.gov.in/.../case123')
                    
                    # Update document link
                    transformed_case['document_link'] = document_link
                    logger.info(f"Final document_link for case {transformed_case['case_number']}: {document_link}")
                    
                    cases.append(CaseResponse(**transformed_case))
                
                return CaseSearchResponse(
                    cases=cases,
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
