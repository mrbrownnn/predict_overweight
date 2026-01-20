from .base import BaseEnum

class YesNoEnum(BaseEnum):
    YES = "yes"
    NO = "no"
    def to_bool(self) -> bool:
        return self == YesNoEnum.YES
    @classmethod
    def from_bool(cls, value: bool) -> 'YesNoEnum':
        return cls.YES if value else cls.NO
