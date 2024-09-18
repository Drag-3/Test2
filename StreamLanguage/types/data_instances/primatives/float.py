from StreamLanguage.types.base import SLType
from StreamLanguage.types.meta_type.primatives.float_type import SLFloatType
from StreamLanguage.types.data_instances.primatives.string import SLString

class SLFloat(SLType):
    type_descriptor = SLFloatType()

    def __init__(self, value):
        if not isinstance(value, float):
            raise TypeError("SLFloat requires a float")
        self.value = value

    def to_slstring(self):
        return SLString(str(self.value))

    def to_python_type(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        if isinstance(other, SLFloat):
            return SLFloat(self.value + other.value)
        return NotImplemented