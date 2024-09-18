from StreamLanguage.ast.symbol_table import SymbolTableEntry
from StreamLanguage.ast.nodes.base import ParserNode
from StreamLanguage.ast.exceptions import ParserError, SLTypeError, VariableNotDeclaredError, SLValueError
from StreamLanguage.exceptions import SLException
from StreamLanguage.types.meta_type.collections.stream_type import SLStreamType
from StreamLanguage.types.meta_type.primatives.boolean_type import SLBooleanType
from StreamLanguage.types.meta_type.primatives.float_type import SLFloatType
from StreamLanguage.types.meta_type.primatives.integer_type import SLIntegerType
from StreamLanguage.types.meta_type.primatives.string_type import SLStringType


class AssignmentNode(ParserNode):
    """
    A node that represents an assignment operation.
    The target is the variable being assigned to.
    The value is the expression whose result will be assigned to the variable.

    Attributes:
        target (IdentifierNode): The variable identifier to which the value is assigned.
        value (ParserNode): The expression that evaluates to the value to be assigned.
    """

    def __init__(self, target, value):
        super().__init__('=')  # Generate a unique UUID for this assignment node
        self.target = target
        self.value = value

    def children(self):
        # Return the target and value as child nodes; these are integral parts of the assignment
        return [self.target, self.value]

    def evaluate(self, context):
        """
        Evaluate the assignment within the given context.
        This method assumes the operation does not create a new block but is a distinct operation.
        """
        try:
            # Evaluate the expression to get the value
            value = self.value.evaluate(context)

            # Check if the target variable is already declared in the context
            if not context.is_declared(self.target.name):
                raise VariableNotDeclaredError(f"Variable '{self.target.name}' not declared")

            # Assign the evaluated value to the target variable
            context.assign(self.target.name, value)

            return value
        except SLException as e:
            # Handle exceptions in a standardized way
            context.handle_exception(e)

    def get_type(self, context):
        # Perform type checking for the assignment, ensuring the types are compatible
        try:
            value_type = self.value.get_type(context)
            if context.is_declared(self.target.name):
                declared_type = context.get_type(self.target.name)
                if declared_type != value_type:
                    raise SLTypeError(f"Type mismatch: cannot assign {value_type.__name__} to {declared_type.__name__}")
            else:
                context.set_type(self.target.name, value_type)
            return value_type
        except SLException as e:
            context.handle_error(e)

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

    def __init__(self, name):
        super().__init__(name)  # Generate a unique UUID for this identifier
        self.name = name

    def children(self):
        # Identifiers typically don't have child nodes as they are the atomic elements of syntax
        return []

    def evaluate(self, context):
        """
        Evaluate the identifier within the given context.
        This typically involves looking up the identifier in the context to retrieve its current value or reference.
        """
        # Check if the identifier exists in the context and retrieve its value
        if not context.is_declared(self.name):
            raise VariableNotDeclaredError(f"Identifier '{self.name}' is not declared")
        return context.lookup(self.name)  # Return the value associated with the identifier


    def get_type(self, context):
        """
        Determine and return the type of the identifier by looking it up in the context.
        This is essential for type checking and ensuring the identifier is used correctly according to its type.
        """
        if context is None:
            raise SLValueError("Context must be provided for type checking")

        if not context.is_declared(self.name):
            raise VariableNotDeclaredError(f"Identifier '{self.name}' is not declared")
        return context.get_type(self.name)  # Return the type of the identifier

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

    def __init__(self, operator, left, right):
        super().__init__(operator)
        self.operator = operator
        self.left = left
        self.right = right

    def children(self):
        return [self.left, self.right]

    def evaluate(self, context):
        left_value = self._extract_value(self.left.evaluate(context))
        right_value = self._extract_value(self.right.evaluate(context))

        return self.perform_operation(left_value, right_value, context)

    def perform_operation(self, left_value, right_value, context):
        def raise_div0():
            raise SLValueError("Division by zero")

        operation_methods = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y if y != 0 else raise_div0(),
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
            return operation_methods[self.operator](left_value, right_value)
        else:
            raise SLValueError(f"Unsupported operator: {self.operator}")

    def get_type(self, context):
        left_type = self.left.get_type(context)
        right_type = self.right.get_type(context)
        if not self.types_are_compatible(left_type, right_type):
            raise SLTypeError(f"Type mismatch in '{self.operator}' operation between {left_type} and {right_type}")

        return self.determine_resultant_type(left_type, right_type)


    def _extract_type(self, entry_type):
        """Extracts the type from a SymbolTableEntry if necessary."""
        if isinstance(entry_type, SymbolTableEntry):
            return entry_type.type
        return entry_type

    def _extract_value(self, entry):
        """Extracts the value from a SymbolTableEntry if necessary."""
        if isinstance(entry, SymbolTableEntry):
            return entry.value
        return entry

    def types_are_compatible(self, left_type, right_type):
        compatible_types = {(SLIntegerType, SLFloatType), (SLFloatType, SLIntegerType)}
        return left_type == right_type or (left_type, right_type) in compatible_types

    def determine_resultant_type(self, left_type, right_type):
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

    def arithmetic_operation_type(self, left_type, right_type):
        # Handle mixed types for arithmetic operations
        if SLIntegerType in [left_type, right_type] and SLFloatType in [left_type, right_type]:
            return SLFloatType
        if left_type == SLIntegerType and right_type == SLIntegerType:
            return SLFloatType if self.operator == '/' else SLIntegerType
        return SLFloatType

    def stream_operation_type(self, left_type, right_type):
        if left_type == SLStreamType and right_type == SLStreamType:
            return SLStreamType
        raise SLTypeError(f"Stream operations not supported between types {left_type} and {right_type}")


    def handle_error(self, error, context):
        error_message = f"Error in binary operation block UUID {self.block_uuid}: {str(error)}"
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

    def __init__(self, operator, operand):
        super().__init__(operator)
        self.operator = operator
        self.operand = operand

    def children(self):
        return [self.operand]

    def evaluate(self, context):
        operand_value = self._extract_value(self.operand.evaluate(context))

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


    def _extract_value(self, entry):
        """Extracts the value from a SymbolTableEntry if necessary."""
        if isinstance(entry, SymbolTableEntry):
            return entry.value
        return entry

    def evaluate_arithmetic(self, operand_value):
        if self.operator == '+':
            return +operand_value
        elif self.operator == '-':
            return -operand_value

    def evaluate_logical(self, operand_value):
        if self.operator == '!':
            return not operand_value

    def evaluate_stream(self, operand_value):
        # Assuming there's a function to convert values to stream objects
        # Placeholder: implement actual logic or call to a library function
        return "to_stream(operand_value)"

    def get_type(self, context):
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

    def _extract_type(self, entry_type):
        """Extracts the type from a SymbolTableEntry if necessary."""
        if isinstance(entry_type, SymbolTableEntry):
            return entry_type.type
        return entry_type


    def handle_error(self, error, context):
        error_message = f"Error in unary operation block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)