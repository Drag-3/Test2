from StreamLanguage.types.base import SLType

class SLInstanceType(SLType):
    """
    Base class for all SL instance types.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def to_python_type(self):
        return self.value