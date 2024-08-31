from .base import ParserNode
from ..exceptions import ParserError

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
        Assign the result of the value node to the target variable in the context.
        """
        try:
            context.enter_block(self.block_uuid)  # Enter the block for this assignment

            # Check if the target is declared in the current scope or any outer scope
            if not context.is_declared(self.target.name):
                raise ParserError(f"Variable '{self.target.name}' not declared", node=self)

            value = self.value.evaluate(context)  # Evaluate the expression to get the value
            context.assign(self.target.name, value)  # Assign the evaluated value to the target variable

            context.exit_block()  # Exit the block for this assignment
            return value
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        """
        Perform type checking for the assignment.
        Update the context with the new type based on the value's type.
        """
        try:
            context.enter_block(self.block_uuid)  # Enter the block for type checking

            # Retrieve the type of the value being assigned
            value_type = self.value.get_type(context)
            # Check if the target is already declared and verify type compatibility
            if context.is_declared(self.target.name):
                declared_type = context.get_type(self.target.name)
                if declared_type is not None and declared_type != value_type:
                    raise TypeError(f"Type mismatch: cannot assign {value_type.__name__} to {declared_type.__name__}")
            # Set the type of the target in the context to the type of the value
            context.set_type(self.target.name, value_type)

            context.exit_block()  # Exit the block for type checking
            return value_type
        except Exception as e:
            self.handle_error(e, context)

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
        super().__init__(name, block_uuid=str(uuid.uuid4()))  # Generate a unique UUID for this identifier
        self.name = name

    def children(self):
        # Identifiers typically don't have child nodes as they are the atomic elements of syntax
        return []

    def evaluate(self, context):
        """
        Evaluate the identifier within the given context.
        This typically involves looking up the identifier in the context to retrieve its current value or reference.
        """
        try:
            context.enter_block(self.block_uuid)  # Enter the block for this identifier evaluation

            # Check if the identifier exists in the context and retrieve its value
            if not context.is_declared(self.name):
                raise NameError(f"Identifier '{self.name}' is not declared")
            value = context.lookup(self.name)

            context.exit_block()  # Exit the block after evaluating the identifier
            return value
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context = None):
        """
        Determine and return the type of the identifier by looking it up in the context.
        This is essential for type checking and ensuring the identifier is used correctly according to its type.
        """
        try:
            if context is None:
                raise ValueError("Context must be provided for type checking")

            context.enter_block(self.block_uuid)  # Enter the block for type checking

            if not context.is_declared(self.name):
                raise NameError(f"Identifier '{self.name}' is not declared")
            identifier_type = context.get_type(self.name)

            context.exit_block()  # Exit the block after type checking
            return identifier_type
        except Exception as e:
            self.handle_error(e, context)

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
        # Evaluate left and right operands
        left_value = self._extract_value(self.left.evaluate(context))
        right_value = self._extract_value(self.right.evaluate(context))

        # Perform the operation
        if self.operator in ['+', '-', '*', '/']:
            return self.evaluate_arithmetic(left_value, right_value)
        elif self.operator in ['&&', '||', '<', '>', '==', '!=', '<=', '>=']:
            return self.evaluate_logical(left_value, right_value)
        elif self.operator in ['>>', '|', '++', '<<']:
            return self.evaluate_stream(left_value, right_value)
        else:
            raise ValueError(f"Unsupported operator: {self.operator}")

    def _extract_value(self, entry):
        """Extracts the value from a SymbolTableEntry if necessary."""
        if isinstance(entry, SymbolTableEntry):
            return entry.value
        return entry

    def evaluate_arithmetic(self, left_value, right_value):
        if self.operator == '+':
            return left_value + right_value
        elif self.operator == '-':
            return left_value - right_value
        elif self.operator == '*':
            return left_value * right_value
        elif self.operator == '/':
            if right_value == 0:
                raise ZeroDivisionError("division by zero")
            return left_value / right_value

    def evaluate_logical(self, left_value, right_value):
        if self.operator == '&&':
            return left_value and right_value
        elif self.operator == '||':
            return left_value or right_value
        elif self.operator == '<':
            return left_value < right_value
        elif self.operator == '>':
            return left_value > right_value
        elif self.operator == '==':
            return left_value == right_value
        elif self.operator == '!=':
            return left_value != right_value
        elif self.operator == '<=':
            return left_value <= right_value
        elif self.operator == '>=':
            return left_value >= right_value

    def evaluate_stream(self, left_value, right_value):
        # Placeholder: Replace with actual logic for handling streams in your system
        if self.operator == '>>':
            return left_value.chain(right_value)
        elif self.operator == '|':
            return left_value.split(right_value)
        elif self.operator == '++':
            return left_value.merge(right_value)
        elif self.operator == '<<':
            return left_value.feedback(right_value)

    def get_type(self, context):
        left_type = self._extract_type(self.left.get_type(context))
        right_type = self._extract_type(self.right.get_type(context))

        if left_type != right_type:
            raise TypeError(f"Type mismatch: cannot perform '{self.operator}' between {left_type.__name__} and {right_type.__name__}")

        # Define type rules for each category of operations
        if self.operator in ['/'] and all(issubclass(t, int) for t in [left_type, right_type]):
            return float
        elif self.operator in ['&&', '||']:
            if left_type == bool and right_type == bool:
                return bool
            else:
                raise TypeError("Logical operations require boolean types")
        elif self.operator in ['>>', '|', '++', '<<']:
            # Stream operations may have specific type requirements or implications
            return self.determine_stream_type(left_type, right_type)
        else:
            return left_type  # For arithmetic and other operations

    def _extract_type(self, entry_type):
        """Extracts the type from a SymbolTableEntry if necessary."""
        if isinstance(entry_type, SymbolTableEntry):
            return entry_type.type
        return entry_type

    def determine_stream_type(self, left_type, right_type):
        # Placeholder: Implement logic for determining the type for stream operations
        return type("Stream", (object,), {})  # Example of a generic Stream type

    def handle_error(self, error, context):
        error_message = f"Error in binary operation block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)



class StreamType:
    pass


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

        if self.operator in ['+', '-']:
            return self.evaluate_arithmetic(operand_value)
        elif self.operator == '!':
            return self.evaluate_logical(operand_value)
        elif self.operator == '.to_stream()':
            return self.evaluate_stream(operand_value)
        else:
            raise ValueError(f"Unsupported unary operator: {self.operator}")

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
        operand_type = self._extract_type(self.operand.get_type(context))

        if self.operator in ['+', '-']:
            return operand_type  # Preserves the type of the operand
        elif self.operator == '!':
            if operand_type != bool:
                raise TypeError("Logical negation requires a boolean type")
            return bool
        elif self.operator == '.to_stream()':
            # Define a type for stream objects if it's a custom class
            return StreamType
        else:
            raise TypeError("Unsupported unary operator for type checking")

    def _extract_type(self, entry_type):
        """Extracts the type from a SymbolTableEntry if necessary."""
        if isinstance(entry_type, SymbolTableEntry):
            return entry_type.type
        return entry_type


    def handle_error(self, error, context):
        error_message = f"Error in unary operation block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)