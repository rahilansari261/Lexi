"""
Custom exceptions for the application
"""

class JagritiAPIException(Exception):
    """Base exception for Jagriti API related errors"""
    pass

class StateNotFoundException(JagritiAPIException):
    """Exception raised when state is not found"""
    def __init__(self, state_name: str):
        self.state_name = state_name
        super().__init__(f"State '{state_name}' not found")

class CommissionNotFoundException(JagritiAPIException):
    """Exception raised when commission is not found"""
    def __init__(self, commission_name: str, state_name: str):
        self.commission_name = commission_name
        self.state_name = state_name
        super().__init__(f"Commission '{commission_name}' not found in state '{state_name}'")

class JagritiAPIError(JagritiAPIException):
    """Exception raised when Jagriti API returns an error"""
    def __init__(self, message: str, status_code: int = None):
        self.status_code = status_code
        super().__init__(message)

class CaseSearchException(JagritiAPIException):
    """Exception raised when case search fails"""
    def __init__(self, message: str, search_type: str = None):
        self.search_type = search_type
        super().__init__(message)
