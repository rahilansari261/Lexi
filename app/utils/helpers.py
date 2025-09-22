"""
Helper functions for data transformation and validation
"""
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def transform_case_data(case_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Transform Jagriti case data to our standardized format
    
    Args:
        case_data: Raw case data from Jagriti API
        
    Returns:
        Transformed case data in our format
    """
    return {
        "case_number": case_data.get("caseNumber") or "",
        "case_stage": case_data.get("caseStageName") or "",
        "filing_date": case_data.get("caseFilingDate") or "",
        "complainant": case_data.get("complainantName") or "",
        "complainant_advocate": case_data.get("complainantAdvocateName") or "",
        "respondent": case_data.get("respondentName") or "",
        "respondent_advocate": case_data.get("respondentAdvocateName") or "",
        "document_link": case_data.get("documentLink") or "https://e-jagriti.gov.in/.../case123"
    }

def validate_date_format(date_string: str) -> bool:
    """
    Validate date string format (YYYY-MM-DD)
    
    Args:
        date_string: Date string to validate
        
    Returns:
        True if valid format, False otherwise
    """
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def sanitize_search_value(search_value: str) -> str:
    """
    Sanitize search value by trimming whitespace and handling special characters
    
    Args:
        search_value: Raw search value
        
    Returns:
        Sanitized search value
    """
    if not search_value:
        return ""
    
    # Trim whitespace
    sanitized = search_value.strip()
    
    # Remove excessive whitespace
    sanitized = " ".join(sanitized.split())
    
    return sanitized

def find_matching_item(items: List[Dict[str, Any]], name_field: str, search_name: str) -> Dict[str, Any]:
    """
    Find matching item in a list by name with fuzzy matching
    
    Args:
        items: List of items to search
        name_field: Field name containing the name to match
        search_name: Name to search for
        
    Returns:
        Matching item or None if not found
    """
    search_name_upper = search_name.upper().strip()
    
    # First try exact match
    for item in items:
        if item.get(name_field, "").upper() == search_name_upper:
            return item
    
    # Then try partial match
    for item in items:
        if search_name_upper in item.get(name_field, "").upper():
            return item
    
    return None

def format_error_message(error: Exception, context: str = "") -> str:
    """
    Format error message with context
    
    Args:
        error: Exception object
        context: Additional context string
        
    Returns:
        Formatted error message
    """
    base_message = str(error)
    if context:
        return f"{context}: {base_message}"
    return base_message
