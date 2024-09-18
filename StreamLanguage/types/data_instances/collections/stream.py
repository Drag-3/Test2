from StreamLanguage.types.base import SLType
from StreamLanguage.types.meta_type.collections.stream_type import SLStreamType
from StreamLanguage.types.data_instances.primatives.string import SLString

class SLStream(SLType):
    type_descriptor = SLStreamType()

    def __init__(self, value):
        if not isinstance(value, list):  # For Now we will assume that a stream is a list Later we will add more functionality
            raise TypeError("SLStream requires a list")
        self.value = value

    def to_slstring(self):
        return SLString(str(self.value))

    def to_python_type(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        if isinstance(other, SLStream):
            return SLStream(self.value + other.value)
        return NotImplemented