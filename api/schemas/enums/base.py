from enum import Enum
from typing import List
class BaseEnum(str, Enum):
    @classmethod
    def values(cls) -> List[str]:
        return [member.value for member in cls]
    
    @classmethod
    def names(cls) -> List[str]:
        return [member.name for member in cls]
    
    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls.values()
    
    @classmethod
    def from_value(cls, value: str) -> 'BaseEnum':
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"'{value}' is not a valid {cls.__name__}")
    
    @classmethod
    def get_description(cls) -> str:
        return cls.__doc__ or cls.__name__
    
    def __str__(self) -> str:
        return self.value
class FrequencyEnum(BaseEnum):
    @classmethod
    def frequency_order(cls) -> List[str]:
        return cls.values()
    
    @classmethod
    def get_frequency_level(cls, value: str) -> int:
        order = cls.frequency_order()
        if value in order:
            return order.index(value)
        return -1
    
    def is_higher_than(self, other: 'FrequencyEnum') -> bool:
        return self.get_frequency_level(self.value) > self.get_frequency_level(other.value)
    
    def is_lower_than(self, other: 'FrequencyEnum') -> bool:
        return self.get_frequency_level(self.value) < self.get_frequency_level(other.value)
