from typing import List
from .base import FrequencyEnum


class CAECEnum(FrequencyEnum):
    """Consumption of food between meals."""
    NO = "no"
    SOMETIMES = "Sometimes"
    FREQUENTLY = "Frequently"
    ALWAYS = "Always"
    
    @classmethod
    def frequency_order(cls) -> List[str]:
        return ["no", "Sometimes", "Frequently", "Always"]


class CALCEnum(FrequencyEnum):
    """Consumption of alcohol."""
    NO = "no"
    SOMETIMES = "Sometimes"
    FREQUENTLY = "Frequently"
    ALWAYS = "Always"
    
    @classmethod
    def frequency_order(cls) -> List[str]:
        return ["no", "Sometimes", "Frequently", "Always"]
