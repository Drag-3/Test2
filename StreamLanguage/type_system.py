from StreamLanguage.sl_types.data_instances.primatives.exception import SLExceptionInstance
from StreamLanguage.sl_types.meta_type.exception_type import SLExceptionType
from StreamLanguage.sl_types.type_registry import TypeRegistry

from StreamLanguage.sl_types.meta_type.primatives.integer_type import SLIntegerType
from StreamLanguage.sl_types.meta_type.primatives.float_type import SLFloatType
from StreamLanguage.sl_types.meta_type.primatives.string_type import SLStringType
from StreamLanguage.sl_types.meta_type.primatives.boolean_type import SLBooleanType

from StreamLanguage.sl_types.meta_type.collections.array_type import SLArrayType
from StreamLanguage.sl_types.meta_type.collections.stack_type import SLStackType
from StreamLanguage.sl_types.meta_type.collections.queue_type import SLQueueType
from StreamLanguage.sl_types.meta_type.collections.stream_type import SLStreamType

from StreamLanguage.sl_types.data_instances.primatives.integer import SLInteger
from StreamLanguage.sl_types.data_instances.primatives.float import SLFloat
from StreamLanguage.sl_types.data_instances.primatives.string import SLString
from StreamLanguage.sl_types.data_instances.primatives.boolean import SLBoolean

from StreamLanguage.sl_types.data_instances.collections.array import SLArray
from StreamLanguage.sl_types.data_instances.collections.stack import SLStack
from StreamLanguage.sl_types.data_instances.collections.queue import SLQueue
from StreamLanguage.sl_types.data_instances.collections.stream import SLStream


def init_type_system():
    """
    Initializes the type system for StreamLanguage.
    """
    # Initialize the type registry
    TypeRegistry.register_type(SLIntegerType(), SLInteger)
    TypeRegistry.register_type(SLFloatType(), SLFloat)
    TypeRegistry.register_type(SLStringType(), SLString)
    TypeRegistry.register_type(SLBooleanType(), SLBoolean)

    TypeRegistry.register_type(SLArrayType(), SLArray)
    TypeRegistry.register_type(SLStackType(), SLStack)
    TypeRegistry.register_type(SLQueueType(), SLQueue)
    TypeRegistry.register_type(SLStreamType(), SLStream)

    # Register conversion functions
    TypeRegistry.register_conversion(SLInteger, SLFloat, lambda x: SLFloat(x.value))
    TypeRegistry.register_conversion(SLFloat, SLInteger, lambda x: SLInteger(x.value))

def init_exception_types():
    """
    Initializes the exception sl_types for StreamLanguage.
    """
    # Define base exception type
    base_exception_type = SLExceptionType("Exception")

    # Register the base exception type
    TypeRegistry.register_type(base_exception_type, SLExceptionInstance)

    # Define specific exception sl_types
    type_error_type = SLExceptionType("TypeError", base=base_exception_type)
    value_error_type = SLExceptionType("ValueError", base=base_exception_type)
    index_error_type = SLExceptionType("IndexError", base=base_exception_type)
    key_error_type = SLExceptionType("KeyError", base=base_exception_type)

    # Register specific exception sl_types
    TypeRegistry.register_type(type_error_type, SLExceptionInstance)
    TypeRegistry.register_type(value_error_type, SLExceptionInstance)
    TypeRegistry.register_type(index_error_type, SLExceptionInstance)
    TypeRegistry.register_type(key_error_type, SLExceptionInstance)

    # Optionally, add constructors to the global namespace
    TypeRegistry._global_namespace["Exception"] = SLExceptionInstance
    TypeRegistry._global_namespace["TypeError"] = SLExceptionInstance
    TypeRegistry._global_namespace["ValueError"] = SLExceptionInstance
    TypeRegistry._global_namespace["IndexError"] = SLExceptionInstance
    TypeRegistry._global_namespace["KeyError"] = SLExceptionInstance
