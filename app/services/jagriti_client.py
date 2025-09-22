"""
Jagriti API client for interacting with the Jagriti portal
"""
import httpx
import logging
from typing import List, Dict, Any, Optional
from app.config import settings
from app.utils.exceptions import (
    JagritiAPIError, 
    StateNotFoundException, 
    CommissionNotFoundException,
    CaseSearchException
)
from app.utils.helpers import find_matching_item, sanitize_search_value

logger = logging.getLogger(__name__)

class JagritiClient:
    """Client for interacting with Jagriti API"""
    
    def __init__(self):
        self.base_url = settings.JAGRITI_BASE_URL
        self.client = httpx.AsyncClient(
            timeout=settings.JAGRITI_TIMEOUT,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
        )
        
    async def get_states(self) -> List[Dict[str, Any]]:
        """
        Get states from Jagriti API
        
        Returns:
            List of state data from Jagriti API
        """
        try:
            api_url = f"{self.base_url}/services/report/report/getStateCommissionAndCircuitBench"
            response = await self.client.get(api_url)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == 200 and data.get("data"):
                # Filter out circuit benches and get main states only
                states = []
                seen_states = set()
                
                for item in data["data"]:
                    commission_name = item.get("commissionNameEn", "")
                    
                    # Filter out circuit benches, regional benches, and other special benches
                    if (not commission_name.startswith("CIRCUIT BENCH") and 
                        not commission_name.startswith("BENCH") and 
                        not commission_name.startswith("REGIONAL BENCH") and
                        not commission_name.startswith("SRINAGAR BENCH") and
                        commission_name not in seen_states):
                        
                        states.append(item)
                        seen_states.add(commission_name)
                
                # Sort states alphabetically
                states.sort(key=lambda x: x.get("commissionNameEn", ""))
                return states
            
            return []
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching states: {e}")
            raise JagritiAPIError(f"Failed to fetch states: {str(e)}")
        except Exception as e:
            logger.error(f"Error fetching states from API: {e}")
            raise JagritiAPIError(f"Failed to fetch states: {str(e)}")

    async def get_commissions(self, state_id: str) -> List[Dict[str, Any]]:
        """
        Get commissions for a state from Jagriti API
        
        Args:
            state_id: State commission ID
            
        Returns:
            List of commission data for the state
        """
        try:
            api_url = f"{self.base_url}/services/report/report/getDistrictCommissionByCommissionId"
            params = {"commissionId": state_id}
            
            response = await self.client.get(api_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == 200 and data.get("data"):
                commissions = data["data"]
                # Sort commissions alphabetically
                commissions.sort(key=lambda x: x.get("commissionNameEn", ""))
                return commissions
            
            return []
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching commissions for state {state_id}: {e}")
            raise JagritiAPIError(f"Failed to fetch commissions: {str(e)}")
        except Exception as e:
            logger.error(f"Error fetching commissions for state {state_id}: {e}")
            raise JagritiAPIError(f"Failed to fetch commissions: {str(e)}")

    async def get_case_details_by_search(
        self, 
        commission_id: int, 
        search_type: int, 
        search_value: str, 
        judge_id: str = "",
        page: int = 0, 
        size: int = 30,
        from_date: str = "2025-01-01",
        to_date: str = "2025-09-22"
    ) -> Dict[str, Any]:
        """
        Get case details by search type from Jagriti API
        
        Args:
            commission_id: Commission ID for the district
            search_type: Type of search (1-7)
            search_value: Value to search for
            judge_id: Judge ID (only for judge search)
            page: Page number for pagination
            size: Number of results per page
            from_date: Start date for search
            to_date: End date for search
            
        Returns:
            Search results from Jagriti API
        """
        try:
            api_url = f"{self.base_url}/services/case/caseFilingService/v2/getCaseDetailsBySearchType"
            
            # Sanitize search value
            sanitized_search_value = sanitize_search_value(search_value)
            
            # Prepare request body
            request_body = {
                "commissionId": commission_id,
                "page": page,
                "size": size,
                "fromDate": from_date,
                "toDate": to_date,
                "dateRequestType": 1,
                "serchType": search_type,
                "serchTypeValue": sanitized_search_value,
                "judgeId": judge_id
            }
            
            response = await self.client.post(
                api_url, 
                json=request_body,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == 200:
                return data
            else:
                error_msg = data.get("message", "Search failed")
                logger.error(f"API returned error: {data}")
                raise CaseSearchException(f"Search failed: {error_msg}")
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP error in case search: {e}")
            raise CaseSearchException(f"Search failed: {str(e)}")
        except CaseSearchException:
            raise
        except Exception as e:
            logger.error(f"Error in case search: {e}")
            raise CaseSearchException(f"Search failed: {str(e)}")

    async def find_state_id_by_name(self, state_name: str) -> int:
        """
        Find state ID by state name
        
        Args:
            state_name: Name of the state
            
        Returns:
            State commission ID
            
        Raises:
            StateNotFoundException: If state is not found
        """
        try:
            states = await self.get_states()
            matching_state = find_matching_item(states, "commissionNameEn", state_name)
            
            if matching_state:
                return matching_state.get("commissionId")
            
            raise StateNotFoundException(state_name)
            
        except StateNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error finding state ID for '{state_name}': {e}")
            raise StateNotFoundException(state_name)

    async def find_commission_id_by_name(self, state_id: int, commission_name: str) -> int:
        """
        Find commission ID by commission name within a state
        
        Args:
            state_id: State commission ID
            commission_name: Name of the commission
            
        Returns:
            Commission ID
            
        Raises:
            CommissionNotFoundException: If commission is not found
        """
        try:
            commissions = await self.get_commissions(str(state_id))
            matching_commission = find_matching_item(commissions, "commissionNameEn", commission_name)
            
            if matching_commission:
                return matching_commission.get("commissionId")
            
            # Get state name for error message
            states = await self.get_states()
            state_name = "Unknown"
            for state in states:
                if state.get("commissionId") == state_id:
                    state_name = state.get("commissionNameEn", "Unknown")
                    break
            
            raise CommissionNotFoundException(commission_name, state_name)
            
        except CommissionNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error finding commission ID for '{commission_name}': {e}")
            raise CommissionNotFoundException(commission_name, "Unknown")

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
