"""
Tests for models
"""
import pytest
from app.models.case import CaseSearchRequest, CaseResponse
from app.models.state import StateResponse
from app.models.commission import CommissionResponse

def test_case_search_request():
    """Test CaseSearchRequest model"""
    request = CaseSearchRequest(
        state="KARNATAKA",
        commission="Bangalore 1st & Rural Additional",
        search_value="test"
    )
    assert request.state == "KARNATAKA"
    assert request.commission == "Bangalore 1st & Rural Additional"
    assert request.search_value == "test"
    assert request.page == 0
    assert request.size == 30

def test_case_response():
    """Test CaseResponse model"""
    case = CaseResponse(
        case_number="123/2025",
        case_stage="Hearing",
        filing_date="2025-02-01",
        complainant="John Doe",
        complainant_advocate="Adv. Reddy",
        respondent="XYZ Ltd.",
        respondent_advocate="Adv. Mehta",
        document_link="https://example.com/case123"
    )
    assert case.case_number == "123/2025"
    assert case.case_stage == "Hearing"

def test_state_response():
    """Test StateResponse model"""
    state = StateResponse(
        commissionId=11290000,
        commissionNameEn="KARNATAKA",
        circuitAdditionBenchStatus=False,
        activeStatus=True
    )
    assert state.commissionId == 11290000
    assert state.commissionNameEn == "KARNATAKA"
