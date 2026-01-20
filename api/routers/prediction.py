from fastapi import APIRouter, HTTPException, status, Depends

from schemas import PredictionInput, PredictionOutput, ErrorResponse
from services import model_service
from core.logging import get_logger
from core.security import verify_api_key

logger = get_logger(__name__)

router = APIRouter(tags=["Prediction"])


@router.post(
    "/predict",
    response_model=PredictionOutput,
    dependencies=[Depends(verify_api_key)],
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Missing API Key"},
        403: {"model": ErrorResponse, "description": "Invalid API Key"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
        503: {"model": ErrorResponse, "description": "Model Not Available"},
    },
    summary="Predict obesity level",
    description="Predict obesity level based on eating habits and physical condition"
)
async def predict(input_data: PredictionInput):
    """
    Predict obesity level based on input features.
    
    **Input Parameters:**
    - Gender: Male or Female
    - Age: Age in years (10-120)
    - Height: Height in meters (1.0-2.5)
    - Weight: Weight in kilograms (20-300)
    - family_history_with_overweight: yes/no
    - FAVC: Frequent consumption of high caloric food (yes/no)
    - FCVC: Frequency of consumption of vegetables (1-3)
    - NCP: Number of main meals (1-4)
    - CAEC: Consumption of food between meals
    - SMOKE: Do you smoke? (yes/no)
    - CH2O: Daily water consumption (1-3 liters)
    - SCC: Calories consumption monitoring (yes/no)
    - FAF: Physical activity frequency (0-3 days/week)
    - TUE: Time using technology devices (0-2 hours)
    - CALC: Consumption of alcohol
    - MTRANS: Transportation used
    
    **Returns:**
    - Predicted obesity level
    - Probability distribution for all 7 categories
    - Confidence score
    - Calculated BMI with category
    """
    if not model_service.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded. Please check if model file exists.",
        )
    
    try:
        # Convert input to dictionary
        input_dict = input_data.model_dump()
        
        # Convert enum values to strings
        for key, value in input_dict.items():
            if hasattr(value, 'value'):
                input_dict[key] = value.value
        
        # Make prediction
        result = model_service.predict(input_dict)
        
        return PredictionOutput(**result)
        
    except ValueError as e:
        logger.error(f"Value error during prediction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input values: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )
