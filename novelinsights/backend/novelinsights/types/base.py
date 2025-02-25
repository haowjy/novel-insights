# Standard library imports
from enum import Enum


class DescribedEnum(str, Enum):
    _description: str  # Add a class-level type annotation
    
    def _generate_next_value_(name, start, count, last_values):
        return name.upper()

    def __new__(cls, value, description: str):
        obj = str.__new__(cls, value)
        obj._value_ = value
        object.__setattr__(obj, '_description', description)
        return obj
    
    @property
    def description(self):
        return self._description
    
    @classmethod
    def all_descriptions(cls) -> str:
        return f"{cls.__name__}: " + ", ".join(
            f"{member.value}: {member.description}" for member in cls.__members__.values()
        )