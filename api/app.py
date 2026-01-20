import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from core.config import settings
from core.logging import get_logger
from services import model_service
from routers import health_router, prediction_router, info_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    logger.info("Starting Obesity Prediction API...")
    os.makedirs(settings.MODEL_DIR, exist_ok=True)
    model_service.load_model()
    yield


# Initialize FastAPI
app = FastAPI(
    title=settings.APP_TITLE,
    description="""
    ## Obesity Level Prediction API
    
    This API predicts obesity levels based on eating habits and physical condition.
    
    ### Features:
    - Predict obesity level from 7 categories
    - Returns probability distribution for each category
    - Calculates and returns BMI
    - Input validation with detailed error messages
    
    ### Obesity Levels:
    1. Insufficient Weight
    2. Normal Weight
    3. Overweight Level I
    4. Overweight Level II
    5. Obesity Type I
    6. Obesity Type II
    7. Obesity Type III
    """,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Handle validation errors globally"""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Input validation error",
            "errors": exc.errors(),
        },
    )


# Include routers
app.include_router(health_router)
app.include_router(prediction_router)
app.include_router(info_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
