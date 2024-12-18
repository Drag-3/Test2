from StreamLanguage.sl_ast.nodes.base import ParserNode
from StreamLanguage.sl_ast.exceptions import ParserError, VariableRedeclaredError, SLTypeError
from StreamLanguage.sl_ast.block_types import BlockType
from StreamLanguage.exceptions import SLException
from StreamLanguage.interpreter.contextN import Context
from StreamLanguage.sl_types.base import SLType


class ProgramNode(ParserNode):
    def __init__(self, nodes):
        super().__init__('program')
        self.nodes = nodes

    def children(self) -> list['ParserNode']:
        return self.nodes

    def evaluate(self, context):
        try:
            with context.block_context(BlockType.PROGRAM, self.block_uuid):
                for node in self.nodes:
                    node.evaluate(context)
                    # Check for control flow signals
                    if context.control_flow.should_return:
                        context.control_flow.should_return = False
                        context.control_flow.return_value = None
                        raise ParserError("Return statement outside function", node=node)
                    if context.control_flow.should_break or context.control_flow.should_continue:
                        # Reset break and continue signals
                        context.control_flow.should_break = False
                        context.control_flow.should_continue = False
                        raise ParserError(f"{'Break' if context.control_flow.should_break else 'Continue'} statement outside loop", node=node)
        except SLException as e:
            self.handle_error(e, context)

    def get_type(self, context):
        try:
            for node in self.nodes:
                node.get_type(context)
        except SLException as e:
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
        children = [self.identifier]
        if self.value:
            children.append(self.value)
        return children

    def evaluate(self, context: Context):
        try:
            # Check if the variable is already declared in the current scope
            if context.current_symbol_table.is_declared(self.identifier.name):
                raise VariableRedeclaredError(f"Variable '{self.identifier.name}' already declared in the current scope")

            # If a value is provided, evaluate it and assign it to the variable
            if self.value:
                value = self.value.evaluate(context)
                value_type = value.type_descriptor

                # If a type hint is provided, check for type compatibility
                if self.type_hint and value_type != self.type_hint:
                    raise SLTypeError(f"Type mismatch: Variable '{self.identifier.name}' expected type {self.type_hint}, but got {value_type}")

                context.declare_variable(self.identifier.name, t=value_type, v=value)
            else:
                # If no value is provided, declare the variable with the type hint or None
                value_type = self.type_hint or None
                value = None
                context.declare_variable(self.identifier.name, t=value_type, v=value)
        except SLException as e:
            self.handle_error(e, context)

    def get_type(self, context):
        if self.type_hint:
            return self.type_hint
        elif self.value:
            return self.value.get_type(context)
        return None

    def handle_error(self, error, context):
        error_message = f"Error in variable declaration '{self.identifier.name}' with block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)