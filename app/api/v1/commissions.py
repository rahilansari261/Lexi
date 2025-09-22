"""
Commission-related API endpoints
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from app.models.commission import CommissionsResponse
from app.api.dependencies import get_jagriti_client
from app.utils.exceptions import JagritiAPIError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/commissions", tags=["commissions"])

@router.get("/{state_id}", response_model=CommissionsResponse)
async def get_commissions(state_id: str, jagriti_client=Depends(get_jagriti_client)):
    """
    Get all district commissions for a specific state
    
    - **state_id**: The commission ID of the state (e.g., 11290000 for Karnataka)
    
    Returns a list of all district commissions for the specified state.
    """
    try:
        commissions_data = await jagriti_client.get_commissions(state_id)
        return CommissionsResponse(commissions=commissions_data)
    except JagritiAPIError as e:
        logger.error(f"Jagriti API error fetching commissions for state {state_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch commissions: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error fetching commissions for state {state_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
