from StreamLanguage.types.base import SLType
from StreamLanguage.types.meta_type.collections.queue_type import SLQueueType
from StreamLanguage.types.data_instances.primatives.string import SLString

class SLQueue(SLType):
    type_descriptor = SLQueueType()

    def __init__(self, value):
        if not isinstance(value, list):
            raise TypeError("SLQueue requires a list")
        self.value = value

    def to_slstring(self):
        return SLString(str(self.value))

    def to_python_type(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        if isinstance(other, SLQueue):
            return SLQueue(self.value + other.value)
        return NotImplemented