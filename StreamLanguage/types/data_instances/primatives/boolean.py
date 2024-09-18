from StreamLanguage.types.base import SLType
from StreamLanguage.types.meta_type.primatives.boolean_type import SLBooleanType
from StreamLanguage.types.data_instances.primatives.string import SLString


class SLBoolean(SLType):
    type_descriptor = SLBooleanType()

    def __init__(self, value):
        if not isinstance(value, bool):
            raise TypeError("SLBoolean requires a boolean")
        self.value = value

    def to_slstring(self):
        return SLString(str(self.value))

    def to_python_type(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        if isinstance(other, SLBoolean):
            return SLBoolean(self.value + other.value)
        return NotImplemented