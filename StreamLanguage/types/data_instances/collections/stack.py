from StreamLanguage.types.base import SLType
from StreamLanguage.types.meta_type.collections.stack_type import SLStackType
from StreamLanguage.types.data_instances.primatives.string import SLString

class SLStack(SLType):
    type_descriptor = SLStackType()

    def __init__(self, value):
        if not isinstance(value, list):
            raise TypeError("SLStack requires a list")
        self.value = value

    def to_slstring(self):
        return SLString(str(self.value))

    def to_python_type(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        if isinstance(other, SLStack):
            return SLStack(self.value + other.value)
        return NotImplemented