"""
Case search API endpoints
"""
import logging
import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse
import io
import base64

from app.models.case import CaseSearchRequest, CaseSearchResponse
from app.models.pdf import PDFUploadRequest, PDFUploadResponse
from app.api.dependencies import get_case_service, get_pdf_service
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

# PDF Management Endpoints

@router.post("/upload-document", response_model=PDFUploadResponse)
async def upload_case_document(request: PDFUploadRequest):
    """
    Upload base64 PDF data for a case and return download URL
    """
    try:
        pdf_service = get_pdf_service()
        
        # Generate filename
        safe_case_number = request.case_number.replace("/", "_").replace(" ", "_")
        filename = request.filename or f"case_{safe_case_number}.pdf"
        
        # Store PDF and get download URL
        download_url = pdf_service.store_pdf(request.base64_data, request.case_number)
        
        return PDFUploadResponse(
            success=True,
            case_number=request.case_number,
            document_link=download_url,
            filename=filename,
            message="Document uploaded successfully"
        )
    except Exception as e:
        logger.error(f"Error uploading PDF for case {request.case_number}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/download/{filename}")
async def download_document(filename: str):
    """
    Download PDF document by filename
    """
    try:
        pdf_service = get_pdf_service()
        file_path = pdf_service.get_pdf_path(filename)
        
        if not file_path:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return FileResponse(
            path=str(file_path),
            media_type="application/pdf",
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading document {filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Error downloading document: {str(e)}")

@router.get("/download/case/{case_number}")
async def download_case_document(case_number: str):
    """
    Download PDF document by case number
    """
    try:
        pdf_service = get_pdf_service()
        file_path = pdf_service.get_pdf_by_case_number(case_number)
        
        if not file_path:
            raise HTTPException(status_code=404, detail="Document not found for this case")
        
        # Generate filename for download
        safe_case_number = case_number.replace("/", "_").replace(" ", "_")
        filename = f"case_{safe_case_number}.pdf"
        
        return FileResponse(
            path=str(file_path),
            media_type="application/pdf",
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading document for case {case_number}: {e}")
        raise HTTPException(status_code=500, detail=f"Error downloading document: {str(e)}")
