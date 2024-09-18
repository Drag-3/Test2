from StreamLanguage.types.base import SLType
from StreamLanguage.types.meta_type.primatives.string_type import SLStringType

class SLString(SLType):
    type_descriptor = SLStringType()

    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError("SLString requires a string")
        self.value = value

    def to_slstring(self):
        return SLString(str(self.value))

    def to_python_type(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        if isinstance(other, SLString):
            return SLString(self.value + other.value)
        return NotImplemented