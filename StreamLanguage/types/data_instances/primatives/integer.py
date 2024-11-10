from StreamLanguage.types.data_instances.instance_base import SLInstanceType
from StreamLanguage.types.meta_type.meta_base import SLMetaType


class SLInteger(SLInstanceType):
    type_descriptor = None  # Will be set when SLIntegerType is initialized

    def __init__(self, value):
        if isinstance(value, SLInteger):
            self.value = value.value  # Same instance, avoid duplication
        elif isinstance(value, int):
            self.value = value
        else:
            from StreamLanguage.types.data_instances.primatives.float import SLFloat
            if isinstance(value, SLFloat):
                self.value = int(value.value)  # Convert SLFloat to SLInteger
            else:
                raise TypeError("SLInteger requires an integer, SLInteger, or SLFloat")

    def to_slstring(self):
        from StreamLanguage.types.data_instances.primatives.string import SLString
        return SLString(str(self.value))

    def __add__(self, other):
        from StreamLanguage.types.data_instances.primatives.float import SLFloat
        if isinstance(other, SLInteger):
            return SLInteger(self.value + other.value)
        if isinstance(other, SLFloat):
            return SLFloat(self.value + other.value)
        return NotImplemented

    def __sub__(self, other):
        from StreamLanguage.types.data_instances.primatives.float import SLFloat
        if isinstance(other, SLInteger):
            return SLInteger(self.value - other.value)
        if isinstance(other, SLFloat):
            return SLFloat(self.value - other.value)
        return NotImplemented

    def __mul__(self, other):
        from StreamLanguage.types.data_instances.primatives.float import SLFloat
        if isinstance(other, SLInteger):
            return SLInteger(self.value * other.value)
        if isinstance(other, SLFloat):
            return SLFloat(self.value * other.value)
        return NotImplemented

    def __truediv__(self, other):
        from StreamLanguage.types.data_instances.primatives.float import SLFloat
        if isinstance(other, SLInteger):
            return SLInteger(self.value / other.value)
        if isinstance(other, SLFloat):
            return SLFloat(self.value / other.value)
        return NotImplemented

    def __floordiv__(self, other):
        from StreamLanguage.types.data_instances.primatives.float import SLFloat
        if isinstance(other, SLInteger):
            return SLInteger(self.value // other.value)
        if isinstance(other, SLFloat):
            return SLFloat(self.value // other.value)
        return NotImplemented

    def __eq__(self, other):
        from StreamLanguage.types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLInteger):
            return SLBoolean(self.value == other.value)
        return NotImplemented

    def __ne__(self, other):
        from StreamLanguage.types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLInteger):
            return SLBoolean(self.value != other.value)
        return NotImplemented

    def __lt__(self, other):
        from StreamLanguage.types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLInteger):
            return SLBoolean(self.value < other.value)
        return NotImplemented

    def __le__(self, other):
        from StreamLanguage.types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLInteger):
            return SLBoolean(self.value <= other.value)
        return NotImplemented

    def __gt__(self, other):
        from StreamLanguage.types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLInteger):
            return SLBoolean(self.value > other.value)
        return NotImplemented

    def __ge__(self, other):
        from StreamLanguage.types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLInteger):
            return SLBoolean(self.value >= other.value)
        return NotImplemented
