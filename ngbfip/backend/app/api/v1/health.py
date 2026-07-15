"""Health check endpoint."""
from fastapi import APIRouter
from app.core.logging import logger

router = APIRouter()


@router.get("/")
async def health_check():
    """Health check endpoint."""
    logger.info("Health check request")
    return {
        "status": "healthy",
        "service": "NG-BIFP Fraud Detection API",
        "version": "1.0.0"
    }
