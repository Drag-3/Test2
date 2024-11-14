from StreamLanguage.sl_types.data_instances.instance_base import SLInstanceType
from StreamLanguage.sl_types.meta_type.meta_base import SLMetaType

class SLString(SLInstanceType):
    type_descriptor = None  # Will be set when SLStringType is initialized

    def __init__(self, value):
        if isinstance(value, SLString):
            self.value = value.value  # Same instance, avoid duplication
        elif isinstance(value, str):
            self.value = value
        else:
            raise TypeError("SLString requires a string")

    def to_slstring(self):
        return self

    def to_python_type(self):
        return self.value

    def __add__(self, other):
        if isinstance(other, SLString):
            return SLString(self.value + other.value)
        return NotImplemented

    def __eq__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLString):
            return SLBoolean(self.value == other.value)
        return NotImplemented

    def __ne__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLString):
            return SLBoolean(self.value != other.value)
        return NotImplemented

    def __lt__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLString):
            return SLBoolean(self.value < other.value)
        return NotImplemented

    def __le__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLString):
            return SLBoolean(self.value <= other.value)
        return NotImplemented

    def __gt__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLString):
            return SLBoolean(self.value > other.value)
        return NotImplemented

    def __ge__(self, other):
        from StreamLanguage.sl_types.data_instances.primatives.boolean import SLBoolean
        if isinstance(other, SLString):
            return SLBoolean(self.value >= other.value)
        return NotImplemented