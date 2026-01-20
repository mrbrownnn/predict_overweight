from typing import List
from .base import BaseEnum
class ObesityLevel(BaseEnum):
    """Obesity level prediction."""
    OVERWEIGHT_LEVEL_II = "Overweight_Level_II"
    NORMAL_WEIGHT = "Normal_Weight"
    INSUFFICIENT_WEIGHT = "Insufficient_Weight"
    OBESITY_TYPE_III = "Obesity_Type_III"
    OBESITY_TYPE_II = "Obesity_Type_II"
    OVERWEIGHT_LEVEL_I = "Overweight_Level_I"
    OBESITY_TYPE_I = "Obesity_Type_I"
    
    @classmethod
    def severity_order(cls) -> List[str]:
        return [
            "Insufficient_Weight",
            "Normal_Weight", 
            "Overweight_Level_I", 
            "Overweight_Level_II",
            "Obesity_Type_I",
            "Obesity_Type_II",
            "Obesity_Type_III" 
        ]
    
    def get_severity_level(self) -> int:
        return self.severity_order().index(self.value)
    
    def is_healthy(self) -> bool:
        return self == ObesityLevel.NORMAL_WEIGHT
    
    def is_overweight_or_obese(self) -> bool:
        return self.get_severity_level() > 1
    
    def is_underweight(self) -> bool:
        return self == ObesityLevel.INSUFFICIENT_WEIGHT
