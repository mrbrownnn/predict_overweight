from .base import BaseEnum

class MTRANSEnum(BaseEnum):
    """Mode of transportation used."""
    AUTOMOBILE = "Automobile"
    BIKE = "Bike"
    MOTORCYCLE = "Motorcycle"
    PUBLIC_TRANSPORT = "Public_Transport"
    WALKING = "Walking"

    def is_active_transport(self) -> bool:
        return self in (MTRANSEnum.BIKE, MTRANSEnum.WALKING)
    
    def is_motorized(self) -> bool:
        return self in (MTRANSEnum.AUTOMOBILE, MTRANSEnum.MOTORBIKE, MTRANSEnum.PUBLIC_TRANSPORTATION)