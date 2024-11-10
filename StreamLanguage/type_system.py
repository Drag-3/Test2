from StreamLanguage.types.type_registry import TypeRegistry

from StreamLanguage.types.meta_type.primatives.integer_type import SLIntegerType
from StreamLanguage.types.meta_type.primatives.float_type import SLFloatType
from StreamLanguage.types.meta_type.primatives.string_type import SLStringType
from StreamLanguage.types.meta_type.primatives.boolean_type import SLBooleanType

from StreamLanguage.types.meta_type.collections.array_type import SLArrayType
from StreamLanguage.types.meta_type.collections.stack_type import SLStackType
from StreamLanguage.types.meta_type.collections.queue_type import SLQueueType
from StreamLanguage.types.meta_type.collections.stream_type import SLStreamType

from StreamLanguage.types.data_instances.primatives.integer import SLInteger
from StreamLanguage.types.data_instances.primatives.float import SLFloat
from StreamLanguage.types.data_instances.primatives.string import SLString
from StreamLanguage.types.data_instances.primatives.boolean import SLBoolean

from StreamLanguage.types.data_instances.collections.array import SLArray
from StreamLanguage.types.data_instances.collections.stack import SLStack
from StreamLanguage.types.data_instances.collections.queue import SLQueue
from StreamLanguage.types.data_instances.collections.stream import SLStream


def init_type_system():
    """
    Initializes the type system for StreamLanguage.
    """
    # Initialize the type registry
    TypeRegistry.register_type(SLIntegerType, SLInteger)
    TypeRegistry.register_type(SLFloatType, SLFloat)
    TypeRegistry.register_type(SLStringType, SLString)
    TypeRegistry.register_type(SLBooleanType, SLBoolean)

    TypeRegistry.register_type(SLArrayType, SLArray)
    TypeRegistry.register_type(SLStackType, SLStack)
    TypeRegistry.register_type(SLQueueType, SLQueue)
    TypeRegistry.register_type(SLStreamType, SLStream)

    # Register conversion functions
    TypeRegistry.register_conversion(SLInteger, SLFloat, lambda x: SLFloat(x.value))
    TypeRegistry.register_conversion(SLFloat, SLInteger, lambda x: SLInteger(x.value))