# Standard library imports
from enum import Enum


class DescribedEnum(str, Enum):
    _description: str  # Add a class-level type annotation

    def __new__(cls, value, description: str):
        obj = object.__new__(cls)
        obj._value_ = value
        object.__setattr__(obj, '_description', description)
        return obj
    
    @property
    def description(self):
        return self._description

