from StreamLanguage.ast.nodes.base import ParserNode
from StreamLanguage.ast.exceptions import ParserError
from StreamLanguage.exceptions import SLException
from StreamLanguage.sl_types.data_instances.collections.array import SLArray
from StreamLanguage.sl_types.meta_type.collections.array_type import SLArrayType
from StreamLanguage.sl_types.meta_type.primatives.boolean_type import SLBooleanType
from StreamLanguage.sl_types.meta_type.primatives.float_type import SLFloatType
from StreamLanguage.sl_types.meta_type.primatives.integer_type import SLIntegerType
from StreamLanguage.sl_types.meta_type.primatives.string_type import SLStringType


class PrimitiveDataNode(ParserNode):
    """
    A node that represents primitive data sl_types, serving as a base class for specific sl_types of primitive data.

    Attributes:
        value: The actual data value stored in the node.
    """

    def __init__(self, value, node_type = None):
        super().__init__(str(value))  # Generate a unique UUID for this primitive data node
        self.value = value
        self.node_type = node_type

    def children(self):
        # Primitive data nodes do not have child nodes as they represent leaf nodes in the AST
        return []

    def evaluate(self, context):
        """
        Evaluate the primitive data node.
        For primitive data nodes, evaluation simply returns the stored value.
        """
        return self.value

    def get_type(self, context):
        """
        Determine and return the type of the primitive data.
        This method must be overridden in subclasses to return the correct type.
        """
        return self.node_type

    def handle_error(self, error, context):
        error_message = f"Error in primitive data node with block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)


class PrimitiveIntNode(PrimitiveDataNode):
    def __init__(self, value):
        super().__init__(value, SLIntegerType())


class PrimitiveFloatNode(PrimitiveDataNode):
    def __init__(self, value):
        super().__init__(value, SLFloatType())


class PrimitiveStringNode(PrimitiveDataNode):
    def __init__(self, value):
        super().__init__(value, SLStringType())


class PrimitiveBoolNode(PrimitiveDataNode):
    def __init__(self, value):
        super().__init__(value, SLBooleanType())


class ArrayNode(ParserNode):
    def __init__(self, elements):
        super().__init__('array')
        self.elements = elements

    def children(self):
        return self.elements

    def evaluate(self, context):
        try:
            # Evaluate each element
            result = []
            for element in self.elements:
                value = element.evaluate(context)
                # Check for control flow signals
                if context.control_flow.should_return or context.control_flow.should_break or context.control_flow.should_continue:
                    # Propagate the signal upwards
                    return
                result.append(value)
            return SLArray(result)
        except SLException as e:
            self.handle_error(e, context)

    def get_type(self, context):
        try:
            if not self.elements:
                result_type = None  # Empty array; type cannot be inferred
            else:
                element_type = self.elements[0].get_type(context)
                for element in self.elements:
                    current_type = element.get_type(context)
                    if current_type != element_type:
                        raise ParserError("Array elements must have the same type", node=self)
                # Use an ArrayType to represent the type of the array
                result_type = SLArrayType(element_type)
            return result_type
        except SLException as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in array node: {str(error)}"
        raise ParserError(error_message, node=self)
