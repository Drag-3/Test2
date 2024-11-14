from StreamLanguage.sl_types.meta_type.meta_base import SLMetaType

class SLExceptionType(SLMetaType):
    """
    Represents the exception meta type in StreamLanguage.
    """

    def __init__(self, name, base=None):
        super().__init__(name)
        self.base = base  # Optional base exception type for inheritance

    def is_subtype_of(self, other):
        """
        Check if this exception type is a subtype of another exception type.
        """
        current = self
        while current:
            if current == other:
                return True
            current = current.base
        return False

    def __eq__(self, other):
        if isinstance(other, SLExceptionType):
            return self.name == other.name
        return False

    def __str__(self):
        return f"ExceptionType: {self.name}"

    def __hash__(self):
        return hash(self.name)

