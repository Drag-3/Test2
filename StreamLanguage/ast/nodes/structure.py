from .base import ParserNode
from ..exceptions import ParserError

class ProgramNode(ParserNode):
    def __init__(self, nodes):
        super().__init__('program')
        self.nodes = nodes  # List of ParserNodes representing the program statements

    def children(self) -> list['ParserNode']:
        return self.nodes

    def evaluate(self, context):
        try:
            for node in self.nodes:
                node.evaluate(context)
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        try:
            for node in self.nodes:
                node.get_type(context)
        except Exception as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in program block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)

class VariableDeclarationNode(ParserNode):
    """
    A node that represents a variable declaration.
    - identifier (IdentifierNode): The name of the variable being declared.
    - type_hint (type, optional): Optional type hint for the variable, for statically typed languages or type inference.
    - value (ParserNode, optional): The initial value assigned to the variable.

    Attributes:
        identifier (IdentifierNode): The identifier node for the variable name.
        type_hint (type): Optional type hint for the variable.
        value (ParserNode): Optional initial value node.
    """

    def __init__(self, identifier, type_hint=None, value=None):
        super().__init__('var_decl')
        self.identifier = identifier
        self.type_hint = type_hint
        self.value = value

    def children(self):
        # Return the identifier and value as child nodes if a value is provided
        children = [self.identifier]
        if self.value:
            children.append(self.value)
        return children

    def evaluate(self, context):
        """
        Evaluate the variable declaration within the given context.
        This involves optionally initializing the variable and updating the context with its value and type.
        This evaluation does not return a value, as it is a declaration statement.
        """
        try:
            # Check if the variable is already declared in the current scope
            if context.is_declared(self.identifier.name):
                raise ParserError(f"Variable '{self.identifier.name}' already declared", node=self)

            # If a value is provided, evaluate it and assign it to the variable
            if self.value is not None:
                value = self.value.evaluate(context)
                context.declare_variable(self.identifier.name, type(value))
                context.assign(self.identifier.name, value)
            else:
                # If no value is provided, just declare the variable with the optional type hint
                context.declare_variable(self.identifier.name, self.type_hint or None)
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        """
        Determine and return the type of the variable being declared.
        This might be the type hint if provided, or the type of the initial value.
        """
        try:
            context.enter_block(self.block_uuid)  # Enter the block for type checking

            if self.type_hint:
                result_type = self.type_hint
            elif self.value:
                result_type = self.value.get_type(context)
            else:
                result_type = None  # If no type hint or initial value, the type may be undetermined

            context.exit_block()  # Exit the block after type checking
            return result_type
        except Exception as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in variable declaration '{self.identifier.name}' with block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)