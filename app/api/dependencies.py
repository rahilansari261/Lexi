"""
API dependencies
"""
from app.services.jagriti_client import JagritiClient
from app.services.case_service import CaseService

# Global instances
_jagriti_client = None
_case_service = None

def get_jagriti_client() -> JagritiClient:
    """Get Jagriti client instance"""
    global _jagriti_client
    if _jagriti_client is None:
        _jagriti_client = JagritiClient()
    return _jagriti_client

def get_case_service() -> CaseService:
    """Get case service instance"""
    global _case_service
    if _case_service is None:
        _case_service = CaseService(get_jagriti_client())
    return _case_service

async def cleanup_dependencies():
    """Cleanup dependencies on app shutdown"""
    global _jagriti_client
    if _jagriti_client:
        await _jagriti_client.close()
        _jagriti_client = None
