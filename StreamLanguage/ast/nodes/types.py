from StreamLanguage.ast.nodes.base import ParserNode
from StreamLanguage.ast.exceptions import ParserError
from StreamLanguage.exceptions import SLException
from StreamLanguage.types.meta_type.primatives.boolean_type import SLBooleanType
from StreamLanguage.types.meta_type.primatives.float_type import SLFloatType
from StreamLanguage.types.meta_type.primatives.integer_type import SLIntegerType
from StreamLanguage.types.meta_type.primatives.string_type import SLStringType


class PrimitiveDataNode(ParserNode):
    """
    A node that represents primitive data types, serving as a base class for specific types of primitive data.

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
        try:
            context.enter_block(self.block_uuid)  # Enter the block for this primitive data evaluation
            result = self.value
            context.exit_block()  # Exit the block after evaluation
            return result
        except SLException as e:
            self.handle_error(e, context)

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
        super().__init__(value, SLBooleanType)


class ArrayNode(ParserNode):
    def __init__(self, elements):
        super().__init__('array')  # Generate a unique UUID for this array node
        self.elements = elements  # List of ParserNodes representing the array elements

    def children(self):
        return self.elements

    def evaluate(self, context):
        """
        Evaluate the array node within the given context.
        This method evaluates each element in the array and returns the list of evaluated elements.
        """
        try:
            context.enter_block(self.block_uuid)  # Enter the block for this array evaluation
            result = [element.evaluate(context) for element in self.elements]
            context.exit_block()  # Exit the block after evaluation
            return result
        except SLException as e:
            self.handle_error(e, context)

    def get_type(self, context):
        """
        Determine and return the type of the array.
        The array type is inferred from the type of its elements. If the array is empty, the type is undetermined.
        """
        try:
            context.enter_block(self.block_uuid)  # Enter the block for type checking

            if not self.elements:
                result_type = None  # Empty array, type cannot be inferred
            else:
                element_type = self.elements[0].get_type(context)
                for element in self.elements:
                    if element.get_type(context) != element_type:
                        raise ParserError("Array elements must have the same type", node=self)
                result_type = [element_type]  # Return a list type with the inferred element type

            context.exit_block()  # Exit the block after type checking
            return result_type
        except SLException as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in array node with block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)