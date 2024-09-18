from StreamLanguage.types.base import SLType

class SLStackType(SLType):
    def to_python_type(self):
        # This method would conceptually return the Python equivalent type for system-level operations.
        return list

    def __str__(self):
        return "SLStack"