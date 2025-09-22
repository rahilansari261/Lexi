"""
CORS middleware configuration
"""
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

def setup_cors(app):
    """Setup CORS middleware for the FastAPI app"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )
