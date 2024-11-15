from StreamLanguage.sl_types.base import SLType
from StreamLanguage.sl_types.data_instances.instance_base import SLInstanceType


class SLFloat(SLInstanceType):
    type_descriptor = None  # Will be set when SLFloatType is initialized

    def __init__(self, value):
        if isinstance(value, SLFloat):
            self.value = value.value  # Same instance, avoid duplication
        elif isinstance(value, float):
            self.value = value
        elif isinstance(value, int):
            self.value = float(value)
        else:
            from StreamLanguage.sl_types.data_instances.primatives.integer import SLInteger
            if isinstance(value, SLInteger):
                self.value = float(value.value)
            else:
                raise TypeError("SLFloat requires a float, SLFloat, or SLInteger")

    def to_slstring(self):
        from StreamLanguage.sl_types.data_instances.primatives.string import SLString
        return SLString(str(self.value))


    def __add__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.integer import SLInteger
        if isinstance(other, SLFloat):
            return SLFloat(self.value + other.value)
        if isinstance(other, SLInteger):
            return SLFloat(self.value + other.value)
        return NotImplemented

    def __sub__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.integer import SLInteger
        if isinstance(other, SLFloat):
            return SLFloat(self.value - other.value)
        if isinstance(other, SLInteger):
            return SLFloat(self.value - other.value)
        return NotImplemented

    def __mul__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.integer import SLInteger
        if isinstance(other, SLFloat):
            return SLFloat(self.value * other.value)
        if isinstance(other, SLInteger):
            return SLFloat(self.value * other.value)
        return NotImplemented

    def __truediv__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.integer import SLInteger
        if isinstance(other, SLFloat):
            return SLFloat(self.value / other.value)
        if isinstance(other, SLInteger):
            return SLFloat(self.value / other.value)
        return NotImplemented

    def __floordiv__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.integer import SLInteger
        if isinstance(other, SLFloat):
            return SLFloat(self.value // other.value)
        if isinstance(other, SLInteger):
            return SLFloat(self.value // other.value)
        return NotImplemented

    def __mod__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.integer import SLInteger
        if isinstance(other, SLFloat):
            return SLFloat(self.value % other.value)
        if isinstance(other, SLInteger):
            return SLFloat(self.value % other.value)
        return NotImplemented

    def __pow__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.integer import SLInteger
        if isinstance(other, SLFloat):
            return SLFloat(self.value ** other.value)
        if isinstance(other, SLInteger):
            return SLFloat(self.value ** other.value)
        return NotImplemented

    def __eq__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.boolean import SLBoolean
        from StreamLanguage.sl_types.data_instances.primatives.integer import SLInteger
        if isinstance(other, SLFloat):
            return SLBoolean(self.value == other.value)
        elif isinstance(other, SLInteger):
            return SLBoolean(self.value == other.value)
        elif isinstance(other, int):
            return SLBoolean(self.value == other)
        elif isinstance(other, float):
            return SLBoolean(self.value == other)
        elif isinstance(other, SLType):
            return SLBoolean(False)
        return NotImplemented

    def __ne__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLFloat):
            return SLBoolean(self.value != other.value)
        return NotImplemented

    def __lt__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLFloat):
            return SLBoolean(self.value < other.value)
        return NotImplemented

    def __le__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLFloat):
            return SLBoolean(self.value <= other.value)
        return NotImplemented

    def __gt__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLFloat):
            return SLBoolean(self.value > other.value)
        return NotImplemented

    def __ge__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLFloat):
            return SLBoolean(self.value >= other.value)
        return NotImplemented

    def __neg__(self):
        return SLFloat(-self.value)

    def __pos__(self):
        return SLFloat(+self.value)

    def __abs__(self):
        return SLFloat(abs(self.value))
