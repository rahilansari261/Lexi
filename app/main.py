"""
Main FastAPI application
"""
import logging
from fastapi import FastAPI
from app.config import settings
from app.middleware.cors import setup_cors
from app.api.v1 import states, commissions, cases
from app.api.dependencies import cleanup_dependencies

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url=settings.API_DOCS_URL,
    redoc_url=settings.API_REDOC_URL,
)

# Setup CORS
setup_cors(app)

# Include routers
app.include_router(states.router)
app.include_router(commissions.router)
app.include_router(cases.router)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": settings.API_TITLE,
        "version": settings.API_VERSION,
        "docs": settings.API_DOCS_URL,
        "redoc": settings.API_REDOC_URL
    }

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on app shutdown"""
    await cleanup_dependencies()
    logger.info("Application shutdown complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
