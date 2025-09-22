"""
Case search API endpoints
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from app.models.case import CaseSearchRequest, CaseSearchResponse
from app.api.dependencies import get_case_service
from app.utils.exceptions import (
    StateNotFoundException, 
    CommissionNotFoundException, 
    CaseSearchException
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cases", tags=["cases"])

@router.post("/by-case-number", response_model=CaseSearchResponse)
async def search_by_case_number(
    request: CaseSearchRequest, 
    case_service=Depends(get_case_service)
):
    """Search cases by case number"""
    try:
        return await case_service.search_by_case_number(request)
    except StateNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CommissionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CaseSearchException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in case number search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/by-complainant", response_model=CaseSearchResponse)
async def search_by_complainant(
    request: CaseSearchRequest, 
    case_service=Depends(get_case_service)
):
    """Search cases by complainant name"""
    try:
        return await case_service.search_by_complainant(request)
    except StateNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CommissionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CaseSearchException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in complainant search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/by-respondent", response_model=CaseSearchResponse)
async def search_by_respondent(
    request: CaseSearchRequest, 
    case_service=Depends(get_case_service)
):
    """Search cases by respondent name"""
    try:
        return await case_service.search_by_respondent(request)
    except StateNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CommissionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CaseSearchException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in respondent search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/by-complainant-advocate", response_model=CaseSearchResponse)
async def search_by_complainant_advocate(
    request: CaseSearchRequest, 
    case_service=Depends(get_case_service)
):
    """Search cases by complainant advocate name"""
    try:
        return await case_service.search_by_complainant_advocate(request)
    except StateNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CommissionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CaseSearchException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in complainant advocate search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/by-respondent-advocate", response_model=CaseSearchResponse)
async def search_by_respondent_advocate(
    request: CaseSearchRequest, 
    case_service=Depends(get_case_service)
):
    """Search cases by respondent advocate name"""
    try:
        return await case_service.search_by_respondent_advocate(request)
    except StateNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CommissionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CaseSearchException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in respondent advocate search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/by-industry-type", response_model=CaseSearchResponse)
async def search_by_industry_type(
    request: CaseSearchRequest, 
    case_service=Depends(get_case_service)
):
    """Search cases by industry type"""
    try:
        return await case_service.search_by_industry_type(request)
    except StateNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CommissionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CaseSearchException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in industry type search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/by-judge", response_model=CaseSearchResponse)
async def search_by_judge(
    request: CaseSearchRequest, 
    case_service=Depends(get_case_service)
):
    """Search cases by judge"""
    try:
        return await case_service.search_by_judge(request)
    except StateNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CommissionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CaseSearchException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in judge search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
