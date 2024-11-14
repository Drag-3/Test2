from StreamLanguage.interpreter.contextN import Context
from StreamLanguage.interpreter.symbol_table import SymbolTableEntry
from StreamLanguage.ast.nodes.base import ParserNode
from StreamLanguage.ast.exceptions import ParserError, SLTypeError, VariableNotDeclaredError, SLValueError
from StreamLanguage.exceptions import SLException
from StreamLanguage.sl_types.base import SLType
from StreamLanguage.sl_types.data_instances.primatives.exception import SLExceptionInstance
from StreamLanguage.sl_types.meta_type.collections.stream_type import SLStreamType
from StreamLanguage.sl_types.meta_type.primatives.boolean_type import SLBooleanType
from StreamLanguage.sl_types.meta_type.primatives.float_type import SLFloatType
from StreamLanguage.sl_types.meta_type.primatives.integer_type import SLIntegerType
from StreamLanguage.sl_types.meta_type.primatives.string_type import SLStringType
from StreamLanguage.sl_types.type_registry import TypeRegistry


class AssignmentNode(ParserNode):
    """
    A node that represents an assignment operation.
    The target is the variable being assigned to.
    The value is the expression whose result will be assigned to the variable.

    Attributes:
        target (IdentifierNode): The variable identifier to which the value is assigned.
        value (ParserNode): The expression that evaluates to the value to be assigned.
    """

    def __init__(self, target: "IdentifierNode", value: ParserNode):
        super().__init__('=')  # Generate a unique UUID for this assignment node
        self.target = target
        self.value = value

    def children(self):
        # Return the target and value as child nodes; these are integral parts of the assignment
        return [self.target, self.value]

    def evaluate(self, context: Context):
        """
        Evaluate the assignment within the given context.
        This method assumes the operation does not create a new block but is a distinct operation.
        """
        # Evaluate the expression to get the value
        value = self.value.evaluate(context)

        # Check for control flow signals
        if (context.control_flow.should_return or context.control_flow.should_break or
                context.control_flow.should_continue or context.control_flow.should_raise):
            # Propagate the signal upwards
            return

        # Check if the target variable is already declared in the current scope
        if not context.current_symbol_table.is_declared(self.target.name):
            error_message = f"Variable '{self.target.name}' not declared"
            raise VariableNotDeclaredError(error_message)

        # Assign the evaluated value to the target variable
        context.assign(self.target.name, value)

        return value

    def get_type(self, context: Context):
        # Perform type checking for the assignment, ensuring the sl_types are compatible
        value_type = self.value.get_type(context)

        if context.current_symbol_table.is_declared(self.target.name):
            declared_type = context.current_symbol_table.lookup_type(self.target.name)
            if declared_type and declared_type != value_type:
                error_message = f"Type mismatch: cannot assign {value_type} to {declared_type}"
                raise SLTypeError(error_message)
        else:
            # Declare the variable with the type of the value
            context.current_symbol_table.declare(self.target.name, t=value_type, v=None)

        return value_type

    def handle_error(self, error, context):
        error_message = f"Assignment error in block UUID {self.block_uuid} at variable '{self.target.name}': {str(error)}"
        raise ParserError(error_message, node=self)


class IdentifierNode(ParserNode):
    """
    A node that represents an identifier, which could be a variable name, a function name,
    or any named entity in the language.

    Attributes:
        name (str): The name of the identifier.
    """

    def __init__(self, name: str):
        super().__init__(name)  # Generate a unique UUID for this identifier
        self.name = name

    def children(self):
        # Identifiers typically don't have child nodes as they are the atomic elements of syntax
        return []

    def evaluate(self, context: Context):
        """
        Evaluate the identifier within the given context.
        This typically involves looking up the identifier in the context to retrieve its current value or reference.
        """
        try:
            value = context.lookup(self.name)
            return value
        except VariableNotDeclaredError as e:
            self.handle_error(e, context)


    def get_type(self, context: Context):
        """
        Determine and return the type of the identifier by looking it up in the context.
        This is essential for type checking and ensuring the identifier is used correctly according to its type.
        """
        if not context.current_symbol_table.is_declared(self.name):
            error_message = f"Identifier '{self.name}' is not declared"
            raise VariableNotDeclaredError(error_message)
        return context.current_symbol_table.lookup_type(self.name)

    def handle_error(self, error, context):
        error_message = f"Error in identifier node '{self.name}' with block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)


class BinaryOperationNode(ParserNode):
    """
    A node that represents a binary operation, including arithmetic, logical, and special stream operators.
    - Arithmetic: +, -, *, /
    - Logical: &&, || (and other logical operations your language might support)
    - Stream:
        >> (Chain): Chains two operations or streams.
        | (Streamsplit): Splits a stream into multiple paths.
        ++ (Streammerge): Merges multiple streams into one.
        << (Feedback): Creates a feedback loop in stream processing.

    Attributes:
        operator (str): The operator symbol.
        left (ParserNode): The left operand.
        right (ParserNode): The right operand.
    """

    def __init__(self, operator: str, left: ParserNode, right: ParserNode):
        super().__init__(operator)
        self.operator = operator
        self.left = left
        self.right = right

    def children(self):
        return [self.left, self.right]

    def evaluate(self, context: Context):
        # Evaluate left operand
        left_value = self.left.evaluate(context)

        # Check for control flow signals
        if (context.control_flow.should_return or context.control_flow.should_break or
                context.control_flow.should_continue or context.control_flow.should_raise):
            return

        # Evaluate right operand
        right_value = self.right.evaluate(context)

        # Check for control flow signals
        if (context.control_flow.should_return or context.control_flow.should_break or
                context.control_flow.should_continue or context.control_flow.should_raise):
            return

        # Extract values
        left_value = self._extract_value(left_value)
        right_value = self._extract_value(right_value)

        try:
            result = self.perform_operation(left_value, right_value, context)
            return result
        except SLException as e:
            self.handle_error(e, context)

    def perform_operation(self, left_value: SLType, right_value: SLType, context: Context):
        value_error_type = TypeRegistry.get_meta_type_by_name("ValueError")

        def division(a, b):
            """
            Perform division operation with error handling for division by zero.
            I chose to define this as a separate function to handle the special case of division by zero WITHIN the
            execution system of the language. This way, the exception can be caught and handled by the control flow
            by user code and not by the interpreter itself.
            :param a: Left operand
            :param b: Right operand
            :return: Arithmetic result of the division
            """
            if b == 0:
                exception_instance = SLExceptionInstance(value_error_type, "Division by zero")
                # Set the exception in the control flow manager
                context.control_flow.set_exception(exception_instance)
                return None  # Return None or appropriate value
            else:
                return a / b

        operation_methods = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': division,
            '<': lambda x, y: x < y,
            '>': lambda x, y: x > y,
            '==': lambda x, y: x == y,
            '!=': lambda x, y: x != y,
            '<=': lambda x, y: x <= y,
            '>=': lambda x, y: x >= y,
            '&&': lambda x, y: x and y,
            '||': lambda x, y: x or y,
            '>>': lambda x, y: x.chain(y),
            '|': lambda x, y: x.split(y),
            '++': lambda x, y: x.merge(y),
            '<<': lambda x, y: x.feedback(y)

        }

        if self.operator in operation_methods:
            result = operation_methods[self.operator](left_value, right_value)
            if context.control_flow.should_raise:
                return None  # Stop further evaluation
            return result
        else:
            raise SLValueError(f"Unsupported operator: {self.operator}")

    def get_type(self, context: Context):
        left_type = self.left.get_type(context)
        right_type = self.right.get_type(context)
        if not self.types_are_compatible(left_type, right_type):
            raise SLTypeError(f"Type mismatch in '{self.operator}' operation between {left_type} and {right_type}")

        return self.determine_resultant_type(left_type, right_type)


    def _extract_type(self, entry_type: SymbolTableEntry | SLType):
        """Extracts the type from a SymbolTableEntry if necessary."""
        if isinstance(entry_type, SymbolTableEntry):
            return entry_type.type
        return entry_type

    def _extract_value(self, entry: SymbolTableEntry | SLType):
        """Extracts the value from a SymbolTableEntry if necessary."""
        if isinstance(entry, SymbolTableEntry):
            return entry.value
        return entry

    def types_are_compatible(self, left_type: SLType, right_type: SLType):
        compatible_types = {(SLIntegerType, SLFloatType), (SLFloatType, SLIntegerType)}
        return left_type == right_type or (left_type, right_type) in compatible_types

    def determine_resultant_type(self, left_type: SLType, right_type: SLType):
        if self.operator in ['+', '-', '*', '/']:
            return self.arithmetic_operation_type(left_type, right_type)
        elif self.operator in ['&&', '||']:
            return SLBooleanType
        elif self.operator in ['<', '>', '==', '!=', '<=', '>=']:
            return SLBooleanType
        elif self.operator in ['>>', '|', '++', '<<']:
            return self.stream_operation_type(left_type, right_type)
        else:
            raise SLTypeError(f"Unsupported operation '{self.operator}'")

    def arithmetic_operation_type(self, left_type: SLType, right_type: SLType):
        # Handle mixed sl_types for arithmetic operations
        if SLIntegerType in [left_type, right_type] and SLFloatType in [left_type, right_type]:
            return SLFloatType
        if left_type == SLIntegerType and right_type == SLIntegerType:
            return SLFloatType if self.operator == '/' else SLIntegerType
        return SLFloatType

    def stream_operation_type(self, left_type: SLType, right_type: SLType):
        if left_type == SLStreamType and right_type == SLStreamType:
            return SLStreamType
        raise SLTypeError(f"Stream operations not supported between types {left_type} and {right_type}")


    def handle_error(self, error, context: Context):
        error_message = f"Error in binary operation '{self.left} {self.operator} {self.right}': {str(error)}"
        raise ParserError(error_message, node=self)




class UnaryOperationNode(ParserNode):
    """
    A node that represents a unary operation.
    - Arithmetic: +, -
    - Logical: !
    - Stream: .to_stream() (Converts a data source into a stream object)

    Attributes:
        operator (str): The unary operator symbol or method.
        operand (ParserNode): The operand of the operation.
    """

    def __init__(self, operator: str, operand: ParserNode):
        super().__init__(operator)
        self.operator = operator
        self.operand = operand

    def children(self):
        return [self.operand]

    def evaluate(self, context: Context):
        # Evaluate operand
        operand_value = self.operand.evaluate(context)

        # Check for control flow signals
        if (context.control_flow.should_return or context.control_flow.should_break or
                context.control_flow.should_continue or context.control_flow.should_raise):
            return

        # Extract value
        operand_value = self._extract_value(operand_value)

        try:
            # Map operator symbols to corresponding lambda functions for evaluation
            operation_methods = {
                '+': lambda x: +x,
                '-': lambda x: -x,
                '!': lambda x: self.evaluate_logical(x),
                '.to_stream()': lambda x: self.evaluate_stream(x),
            }

            if self.operator in operation_methods:
                return operation_methods[self.operator](operand_value)
            else:
                raise SLValueError(f"Unsupported unary operator: {self.operator}")
        except SLException as e:
            self.handle_error(e, context)


    def _extract_value(self, entry: SymbolTableEntry | SLType):
        """Extracts the value from a SymbolTableEntry if necessary."""
        if isinstance(entry, SymbolTableEntry):
            return entry.value
        return entry

    def evaluate_arithmetic(self, operand_value: SLType):
        if self.operator == '+':
            return +operand_value
        elif self.operator == '-':
            return -operand_value

    def evaluate_logical(self, operand_value: SLType):
        if self.operator == '!':
            return not operand_value

    def evaluate_stream(self, operand_value):
        # Does NOT work yet
        return "to_stream(operand_value)"

    def get_type(self, context: Context):
        operand_type = self.operand.get_type(context)

        # Define type rules for each operation
        type_rules = {
            '+': lambda x: x,
            '-': lambda x: x,
            '!': lambda _: bool,
            '.to_stream()': lambda _: SLStreamType,
        }

        if self.operator in type_rules:
            return type_rules[self.operator](operand_type)
        else:
            raise TypeError(f"Unsupported unary operator for type checking: {self.operator}")

    def _extract_type(self, entry_type: SymbolTableEntry | SLType):
        """Extracts the type from a SymbolTableEntry if necessary."""
        if isinstance(entry_type, SymbolTableEntry):
            return entry_type.type
        return entry_type


    def handle_error(self, error, context: Context):
        error_message = f"Error in unary operation '{self.operator} {self.operand}': {str(error)}"
        raise ParserError(error_message, node=self)