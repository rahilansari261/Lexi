"""
State-related API endpoints
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from app.models.state import StatesResponse
from app.api.dependencies import get_jagriti_client
from app.utils.exceptions import JagritiAPIError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/states", tags=["states"])

@router.get("", response_model=StatesResponse)
async def get_states(jagriti_client=Depends(get_jagriti_client)):
    """
    Get all available states and union territories
    
    Returns a list of all states/UTs from the Jagriti portal with their commission IDs.
    Circuit benches and special benches are filtered out to show only main states.
    """
    try:
        states_data = await jagriti_client.get_states()
        return StatesResponse(states=states_data)
    except JagritiAPIError as e:
        logger.error(f"Jagriti API error fetching states: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch states: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error fetching states: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
