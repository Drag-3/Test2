from StreamLanguage.types.base import SLType
from StreamLanguage.types.meta_type.primatives.integer_type import SLIntegerType


class SLInteger(SLType):
    type_descriptor = SLIntegerType()

    def __init__(self, value):
        if not isinstance(value, int):
            raise TypeError("SLInteger requires an integer")
        self.value = value

    def to_slstring(self):
        return SLString(str(self.value))

    def to_python_type(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        if isinstance(other, SLInteger):
            return SLInteger(self.value + other.value)
        return NotImplemented
