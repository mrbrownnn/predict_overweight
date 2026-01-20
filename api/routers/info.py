from fastapi import APIRouter

from core.constants import LABEL_MAPPING, FEATURES_INFO

router = APIRouter(tags=["Info"])


@router.get("/labels")
async def get_labels():
    """Get all possible obesity level labels"""
    return {
        "labels": LABEL_MAPPING,
        "total_classes": len(LABEL_MAPPING)
    }


@router.get("/features")
async def get_features():
    """Get information about required input features"""
    return {"features": FEATURES_INFO}
