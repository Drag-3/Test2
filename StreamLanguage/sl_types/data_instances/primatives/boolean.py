from StreamLanguage.sl_types.data_instances.instance_base import SLInstanceType
from StreamLanguage.sl_types.meta_type.meta_base import SLMetaType

class SLBoolean(SLInstanceType):
    type_descriptor = None  # Will be set when SLBooleanType is initialized

    def __init__(self, value):
        if isinstance(value, SLBoolean):
            self.value = value.value  # Same instance, avoid duplication
        elif isinstance(value, bool):
            self.value = value
        else:
            raise TypeError("SLBoolean requires a boolean")

    def to_slstring(self):
        from StreamLanguage.sl_types.data_instances.primatives.string import SLString
        return SLString(str(self.value))

    def __bool__(self):
        return self.value

    def __and__(self, other):
        if isinstance(other, SLBoolean):
            return SLBoolean(self.value and other.value)
        return NotImplemented

    def __or__(self, other):
        if isinstance(other, SLBoolean):
            return SLBoolean(self.value or other.value)
        return NotImplemented

    def __xor__(self, other):
        if isinstance(other, SLBoolean):
            return SLBoolean(self.value ^ other.value)
        return NotImplemented

    def __invert__(self):
        return SLBoolean(not self.value)

    def __eq__(self, other):
        if isinstance(other, SLBoolean):
            return SLBoolean(self.value == other.value)
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, SLBoolean):
            return SLBoolean(self.value != other.value)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, SLBoolean):
            return SLBoolean(self.value < other.value)
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, SLBoolean):
            return SLBoolean(self.value <= other.value)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, SLBoolean):
            return SLBoolean(self.value > other.value)
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, SLBoolean):
            return SLBoolean(self.value >= other.value)
        return NotImplemented