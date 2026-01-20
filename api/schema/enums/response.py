from pydantic import BaseModel, Field
class PredictionOutput(BaseModel):
    prediction: str = Field(..., description="Predicted obesity level")
    prediction_code: int = Field(..., description="Numeric code for prediction")
    probabilities: dict = Field(..., description="Probability for each obesity level")
    confidence: float = Field(..., description="Confidence score (max probability)")
    bmi: float = Field(..., description="Calculated BMI from input")
    bmi_category: str = Field(..., description="BMI category description")

    class Config:
        json_schema_extra = {
            "example": {
                "prediction": "Normal_Weight",
                "prediction_code": 1,
                "probabilities": {
                    "Overweight_Level_II": 0.05,
                    "Normal_Weight": 0.80,
                    "Insufficient_Weight": 0.05,
                    "Obesity_Type_III": 0.02,
                    "Obesity_Type_II": 0.03,
                    "Overweight_Level_I": 0.03,
                    "Obesity_Type_I": 0.02
                },
                "confidence": 0.80,
                "bmi": 24.49,
                "bmi_category": "Normal weight"
            }
        }
class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    scaler_loaded: bool
    version: str
class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    error_code: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Invalid input data",
                "error_code": "VALIDATION_ERROR"
            }
        }
