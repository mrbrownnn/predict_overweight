from .health import router as health_router
from .prediction import router as prediction_router
from .info import router as info_router

__all__ = ["health_router", "prediction_router", "info_router"]
