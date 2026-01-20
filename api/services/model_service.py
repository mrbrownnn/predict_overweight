import os
from typing import Optional, Dict, Any
import numpy as np
import pandas as pd
import xgboost as xgb
import joblib

from core.config import settings
from core.constants import LABEL_MAPPING
from core.logging import get_logger

logger = get_logger(__name__)


class ModelService:
    """Service for handling ML model operations"""
    
    def __init__(self):
        self.model: Optional[xgb.XGBClassifier] = None
    
    def load_model(self) -> bool:
        """Load XGBoost model from file"""
        if os.path.exists(settings.MODEL_PATH):
            self.model = xgb.XGBClassifier()
            self.model.load_model(settings.MODEL_PATH)
            logger.info(f"Model loaded successfully from {settings.MODEL_PATH}")
            return True
        
        if os.path.exists(settings.MODEL_PKL_PATH):
            self.model = joblib.load(settings.MODEL_PKL_PATH)
            logger.info(f"Model loaded successfully from {settings.MODEL_PKL_PATH}")
            return True
        
        logger.warning("No model file found")
        return False
    
    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None
    
    def predict(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Make prediction from input dictionary"""
        if not self.is_loaded:
            raise RuntimeError("Model is not loaded")
        
        # Calculate BMI
        height = input_dict['Height']
        weight = input_dict['Weight']
        bmi = weight / (height ** 2)
        bmi_category = self._get_bmi_category(bmi)
        
        # Create DataFrame and predict
        df = pd.DataFrame([input_dict])
        prediction_code = int(self.model.predict(df)[0])
        prediction_label = LABEL_MAPPING.get(prediction_code, "Unknown")
        
        # Get probabilities
        probabilities_array = self.model.predict_proba(df)[0]
        labels = list(LABEL_MAPPING.values())
        probabilities = {
            label: round(float(prob), 4)
            for label, prob in zip(labels, probabilities_array)
        }
        
        confidence = float(np.max(probabilities_array))
        
        logger.info(f"Prediction made: {prediction_label} with confidence {confidence:.2%}")
        
        return {
            "prediction": prediction_label,
            "prediction_code": prediction_code,
            "probabilities": probabilities,
            "confidence": round(confidence, 4),
            "bmi": round(bmi, 2),
            "bmi_category": bmi_category
        }
    
    @staticmethod
    def _get_bmi_category(bmi: float) -> str:
        """Get BMI category from BMI value"""
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        return "Obese"


# Singleton instance
model_service = ModelService()
