import httpx
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class JagritiClient:
    def __init__(self):
        self.base_url = "https://e-jagriti.gov.in"
        self.client = httpx.AsyncClient(
            timeout=30.0,
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
        """Get states from Jagriti API - return data as-is"""
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
            
        except Exception as e:
            logger.error(f"Error fetching states from API: {e}")
            return []

    async def get_commissions(self, state_id: str) -> List[Dict[str, Any]]:
        """Get commissions for a state from Jagriti API - return data as-is"""
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
            
        except Exception as e:
            logger.error(f"Error fetching commissions for state {state_id}: {e}")
            return []

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
        """
        try:
            api_url = f"{self.base_url}/services/case/caseFilingService/v2/getCaseDetailsBySearchType"
            
            # Prepare request body
            request_body = {
                "commissionId": commission_id,
                "page": page,
                "size": size,
                "fromDate": from_date,
                "toDate": to_date,
                "dateRequestType": 1,
                "serchType": search_type,
                "serchTypeValue": search_value,
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
                logger.error(f"API returned error: {data}")
                return {"status": 500, "message": "Search failed", "data": []}
                
        except Exception as e:
            logger.error(f"Error in case search: {e}")
            return {"status": 500, "message": f"Search failed: {str(e)}", "data": []}

    async def find_state_id_by_name(self, state_name: str) -> int:
        """Find state ID by state name"""
        try:
            states = await self.get_states()
            state_name_upper = state_name.upper().strip()
            
            for state in states:
                if state.get("commissionNameEn", "").upper() == state_name_upper:
                    return state.get("commissionId")
            
            # If not found, try partial matching
            for state in states:
                if state_name_upper in state.get("commissionNameEn", "").upper():
                    return state.get("commissionId")
            
            raise ValueError(f"State '{state_name}' not found")
            
        except Exception as e:
            logger.error(f"Error finding state ID for '{state_name}': {e}")
            raise ValueError(f"State '{state_name}' not found")

    async def find_commission_id_by_name(self, state_id: int, commission_name: str) -> int:
        """Find commission ID by commission name within a state"""
        try:
            commissions = await self.get_commissions(str(state_id))
            commission_name_upper = commission_name.upper().strip()
            
            for commission in commissions:
                if commission.get("commissionNameEn", "").upper() == commission_name_upper:
                    return commission.get("commissionId")
            
            # If not found, try partial matching
            for commission in commissions:
                if commission_name_upper in commission.get("commissionNameEn", "").upper():
                    return commission.get("commissionId")
            
            raise ValueError(f"Commission '{commission_name}' not found in state")
            
        except Exception as e:
            logger.error(f"Error finding commission ID for '{commission_name}': {e}")
            raise ValueError(f"Commission '{commission_name}' not found in state")

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
