from StreamLanguage.sl_types.base import SLType

class SLInstanceType(SLType):
    """
    Base class for all SL instance sl_types.
    """
    type_descriptor = None  # Will be set when the type is initialized

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def to_python_type(self):
        return self.value