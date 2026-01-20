import os
import logging
from contextlib import asynccontextmanager
from typing import Optional
import numpy as np
import xgboost as xgb
import joblib
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from schemas import (
    PredictionInput,
    PredictionOutput,
    HealthCheckResponse,
    ErrorResponse,
)
from preprocessing import DataPreprocessor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables for model and preprocessor
model: Optional[xgb.XGBClassifier] = None
preprocessor: Optional[DataPreprocessor] = None

# Model paths
MODEL_DIR = os.getenv("MODEL_DIR", "./models")
MODEL_PATH = os.path.join(MODEL_DIR, "xgb_obesity_model.json")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")


def load_model():
    """Load XGBoost model from file"""
    global model
    
    if os.path.exists(MODEL_PATH):
        model = xgb.XGBClassifier()
        model.load_model(MODEL_PATH)
        return True
    
    else:
        pkl_path = MODEL_PATH.replace('.json', '.pkl')
        if os.path.exists(pkl_path):
            model = joblib.load(pkl_path)
            logger.info(f"Model loaded successfully from {pkl_path}")
            return True



def load_preprocessor():
    """Load preprocessor with scaler"""
    global preprocessor
    
    if os.path.exists(SCALER_PATH):
        preprocessor = DataPreprocessor(scaler_path=SCALER_PATH)
        logger.info(f"Scaler loaded successfully from {SCALER_PATH}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Obesity Prediction API...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    load_model()
    load_preprocessor()
    yield

# Initialize FastAPI 
app = FastAPI(
    title="Obesity Level Prediction API",
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
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
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
# API Endpoints
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Obesity Level Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="healthy" if model is not None else "degraded",
        model_loaded=model is not None,
        scaler_loaded=preprocessor is not None and preprocessor.scaler is not None,
        version="1.0.0"
    )


@app.post(
    "/predict",
    response_model=PredictionOutput,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
        503: {"model": ErrorResponse, "description": "Model Not Available"},
    },
    tags=["Prediction"],
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
    # Check if model is loaded
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded. Please check if model file exists.",
        )
    
    if preprocessor is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Preprocessor is not initialized.",
        )
    
    try:
        # Convert input to dictionary
        input_dict = input_data.model_dump()
        
        # Convert enum values to strings
        for key, value in input_dict.items():
            if hasattr(value, 'value'):
                input_dict[key] = value.value
    
    
    """        # Preprocess input and make prediction """
        bmi = preprocessor.calculate_bmi(input_dict['Height'], input_dict['Weight'])
        bmi_category = preprocessor.get_bmi_category(bmi)
        processed_data = preprocessor.preprocess_input(input_dict)
        prediction_code = int(model.predict(processed_data)[0])
        prediction_label = preprocessor.decode_prediction(prediction_code)
        
        # Get probabilities
        probabilities_array = model.predict_proba(processed_data)[0]
        labels = preprocessor.get_all_labels()
        probabilities = {
            label: round(float(prob), 4)
            for label, prob in zip(labels, probabilities_array)
        }
        
        # Get confidence (max probability)
        confidence = float(np.max(probabilities_array))
        
        logger.info(f"Prediction made: {prediction_label} with confidence {confidence:.2%}")
        
        return PredictionOutput(
            prediction=prediction_label,
            prediction_code=prediction_code,
            probabilities=probabilities,
            confidence=round(confidence, 4),
            bmi=round(bmi, 2),
            bmi_category=bmi_category
        )
        
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


@app.get("/labels", tags=["Info"])
async def get_labels():
    """Get all possible obesity level labels"""
    if preprocessor is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Preprocessor is not initialized."
        )
    
    return {
        "labels": preprocessor.LABEL_MAPPING,
        "total_classes": len(preprocessor.LABEL_MAPPING)
    }


@app.get("/features", tags=["Info"])
async def get_features():
    """Get information about required input features"""
    return {
        "features": {
            "Gender": {"type": "string", "values": ["Male", "Female"]},
            "Age": {"type": "float", "range": [10, 120], "unit": "years"},
            "Height": {"type": "float", "range": [1.0, 2.5], "unit": "meters"},
            "Weight": {"type": "float", "range": [20, 300], "unit": "kg"},
            "family_history_with_overweight": {"type": "string", "values": ["yes", "no"]},
            "FAVC": {"type": "string", "values": ["yes", "no"], "description": "High caloric food consumption"},
            "FCVC": {"type": "float", "range": [1, 3], "description": "Vegetable consumption frequency"},
            "NCP": {"type": "float", "range": [1, 4], "description": "Number of main meals"},
            "CAEC": {"type": "string", "values": ["no", "Sometimes", "Frequently", "Always"], "description": "Food between meals"},
            "SMOKE": {"type": "string", "values": ["yes", "no"]},
            "CH2O": {"type": "float", "range": [1, 3], "unit": "liters", "description": "Daily water intake"},
            "SCC": {"type": "string", "values": ["yes", "no"], "description": "Calorie monitoring"},
            "FAF": {"type": "float", "range": [0, 3], "description": "Physical activity frequency (days/week)"},
            "TUE": {"type": "float", "range": [0, 2], "unit": "hours", "description": "Technology usage time"},
            "CALC": {"type": "string", "values": ["no", "Sometimes", "Frequently", "Always"], "description": "Alcohol consumption"},
            "MTRANS": {"type": "string", "values": ["Automobile", "Motorbike", "Bike", "Public_Transportation", "Walking"], "description": "Transportation"}
        }
    }


# Run with: uvicorn app:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
