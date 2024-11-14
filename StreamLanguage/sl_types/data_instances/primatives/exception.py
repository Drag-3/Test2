from StreamLanguage.sl_types.data_instances.instance_base import SLInstanceType
from StreamLanguage.exceptions import SLException

class SLExceptionInstance(SLInstanceType):
    """
    Represents an exception instance in StreamLanguage.
    """

    def __init__(self, exception_type, message):
        super().__init__(value=None) # No value for exceptions
        self.type_descriptor = exception_type
        self.message = message

    @classmethod
    def constructor(cls, exception_type_name, message):
        from StreamLanguage.sl_types.type_registry import TypeRegistry
        # Get the exception meta type from the TypeRegistry
        exception_type = TypeRegistry.get_meta_type_by_name(exception_type_name)
        if exception_type is None:
            raise SLException(f"Exception type '{exception_type_name}' not found")
        return cls(exception_type, message)


    def to_slstring(self):
        from StreamLanguage.sl_types.data_instances.primatives.string import SLString
        return SLString(self.message)

    def __str__(self):
        return f"{self.type_descriptor.name}: {self.message}"

    def __eq__(self, other):
        if isinstance(other, SLExceptionInstance):
            return self.type_descriptor == other.type_descriptor and self.message == other.message
        return False
