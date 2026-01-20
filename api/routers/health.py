from fastapi import APIRouter

from schemas import HealthCheckResponse
from services import model_service
from core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Obesity Level Prediction API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="healthy" if model_service.is_loaded else "degraded",
        model_loaded=model_service.is_loaded,
        scaler_loaded=False,
        version=settings.APP_VERSION
    )
