class ParserNode:
    def __init__(self, token):
        self.token = token

    def children(self):
        raise NotImplementedError("Each node must implement 'children' method.")

    def evaluate(self, context):
        raise NotImplementedError("Each node must implement 'evaluate' method for execution.")

    def get_type(self, context):
        raise NotImplementedError("Each node must implement 'get_type' method for type checking.")

    def handle_error(self, error, context):
        # Custom method to handle errors; can log or modify error messages here
        raise ParserError(str(error), node=self)


class ProgramNode(ParserNode):
    def __init__(self, nodes):
        super().__init__('program')
        self.nodes = nodes

    def children(self):
        return self.nodes

    def evaluate(self, context):
        for node in self.nodes:
            node.evaluate(context)

    def get_type(self, context):
        for node in self.nodes:
            node.get_type(context)

# Program Structure Nodes
class IfNode(ParserNode):
    """
    A node that represents an if statement.
    - `condition`: The condition to evaluate, which determines which branch to execute.
    - `then_block`: The block of code to execute if the condition is true.
    - `else_block`: The block of code to execute if the condition is false (optional).
    """

    def __init__(self, condition, then_block, else_block=None):
        super().__init__('if')  # Token representing 'if' could just be the keyword 'if'
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def children(self):
        # Return all child nodes, including the else block if it exists
        children = [self.condition, self.then_block]
        if self.else_block:
            children.append(self.else_block)
        return children

    def evaluate(self, context):
        try:
            # If needed, create new contexts for each block to represent new scopes
            if_context = context.clone()  # Clone if block-specific scope is needed
            if self.condition.evaluate(context):
                for node in self.then_block:
                    node.evaluate(if_context)
            elif self.else_block:
                else_context = context.clone()  # Clone if else-specific scope is needed
                for node in self.else_block:
                    node.evaluate(else_context)
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        """
        The type of an if statement can be ambiguous if the branches return different types,
        hence we check the types of both branches and raise an error if they don't match.
        If the if statement doesn't return anything explicitly, it can be considered as having 'None' type.
        """
        try:
            then_type = self.then_block.get_type(context)
            else_type = self.else_block.get_type(context) if self.else_block else None
            if else_type and then_type != else_type:
                raise ParserError("Type mismatch between then and else branches", node=self)
            return then_type
        except Exception as e:
            self.handle_error(e, context)


class WhileNode(ParserNode):
    """
    A node that represents a while loop.
    - `condition`: The condition to evaluate for each loop iteration.
    - `body`: The block of code to execute as long as the condition is true.
    """

    def __init__(self, condition, body):
        super().__init__('while')  # Token representing 'while' could just be the keyword 'while'
        self.condition = condition
        self.body = body

    def children(self):
        # Return both the condition and the body as child nodes
        return [self.condition, self.body]

    def evaluate(self, context):
        """
        Evaluate the while loop within the given context.
        This method repeatedly evaluates the body as long as the condition evaluates to True.
        """
        try:
            loop_context = context.clone()  # Use clone if loop-specific scope is needed
            while self.condition.evaluate(context):
                for node in self.body:
                    node.evaluate(loop_context)
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        """
        The while loop will have None type as it doesn't return a value directly.
        """
        try:
            condition_type = self.condition.get_type(context)
            if condition_type != bool:
                raise ParserError("While loop condition must be a boolean", node=self)
            for node in self.body:
                node.get_type(context)
            return None
        except Exception as e:
            self.handle_error(e, context)

class ForNode(ParserNode):
    def __init__(self, initializer, condition, increment, body):
        super().__init__('for')
        self.initializer = initializer  # Typically an AssignmentNode or VariableDeclarationNode
        self.condition = condition      # Expression node that evaluates to a boolean
        self.increment = increment      # UpdateNode or similar for incrementing/decrementing
        self.body = body                # List of ParserNodes representing the loop body

    def children(self):
        return [self.initializer, self.condition, self.increment] + self.body

    def evaluate(self, context):
        self.initializer.evaluate(context)
        while self.condition.evaluate(context):
            for statement in self.body:
                statement.evaluate(context)
            self.increment.evaluate(context)


# Operation Nodes
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
        super().__init__('=')  # Token for assignment could just be the '=' character
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
            # Check if the target is declared in the current scope or any outer scope
            if not context.is_declared(self.target.name):
                raise ParserError(f"Variable '{self.target.name}' not declared", node=self)

            value = self.value.evaluate(context)
            context.assign(self.target.name, value)
            return value
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        """
        Perform type checking for the assignment.
        Update the context with the new type based on the value's type.
        """
        # Retrieve the type of the value being assigned
        value_type = self.value.get_type(context)
        # Check if the target is already declared and verify type compatibility
        if context.is_declared(self.target.name):
            declared_type = context.get_type(self.target.name)
            if declared_type is not None and declared_type != value_type:
                raise TypeError(f"Type mismatch: cannot assign {value_type.__name__} to {declared_type.__name__}")
        # Set the type of the target in the context to the type of the value
        context.set_type(self.target.name, value_type)
        return value_type



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
        # Basic arithmetic operations
        left_value = self.left.evaluate(context)
        right_value = self.right.evaluate(context)

        if self.operator in ['+', '-', '*', '/']:
            return self.evaluate_arithmetic(left_value, right_value)
        elif self.operator in ['&&', '||']:
            return self.evaluate_logical(left_value, right_value)
        elif self.operator in ['>>', '|', '++', '<<']:
            return self.evaluate_stream(left_value, right_value)
        else:
            raise ValueError(f"Unsupported operator: {self.operator}")

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
        left_type = self.left.get_type(context)
        right_type = self.right.get_type(context)

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

    def determine_stream_type(self, left_type, right_type):
        # I don't have logic for streams yet... still working on it!
        return type("Stream", (object,), {})  # Example of a generic Stream type


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
        # Returns the operand as the only child node
        return [self.operand]

    def evaluate(self, context):
        """
        Evaluate the unary operation within the given context.
        The actual operation performed depends on the operator type.
        """
        operand_value = self.operand.evaluate(context)

        if self.operator in ['+', '-']:
            return self.evaluate_arithmetic(operand_value)
        elif self.operator == '!':
            return self.evaluate_logical(operand_value)
        elif self.operator == '.to_stream()':
            return self.evaluate_stream(operand_value)
        else:
            raise ValueError(f"Unsupported unary operator: {self.operator}")

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
        """
        Determine and return the type of the unary operation.
        Different operations may have different type implications.
        """
        operand_type = self.operand.get_type(context)

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


class FunctionCallNode(ParserNode):
    """
    A node that represents a function call.
    - function (IdentifierNode or similar): Represents the function being called.
    - arguments (list of ParserNode): A list of nodes representing the arguments passed to the function.

    Attributes:
        function (ParserNode): The function identifier or expression resulting in a function.
        arguments (list): A list of expressions representing the function call arguments.
    """

    def __init__(self, function, arguments):
        super().__init__('call')
        self.function = function
        self.arguments = arguments

    def children(self):
        # Returns all nodes related to the function and its arguments
        return [self.function] + self.arguments

    def evaluate(self, context):
        try:
            func = self.function.evaluate(context)
            args_values = [arg.evaluate(context) for arg in self.arguments]
            return func.invoke(args_values, context)
        except RecursionError as re:
            raise ParserError(f"Infinite recursion detected in function '{self.function.name}': {str(re)}", node=self)
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        try:
            # Resolve the function from the context
            func = self.function.evaluate(context)

            # Check if func is actually a function and has a return type
            if not hasattr(func, 'return_type'):
                raise TypeError(f"'{self.function.name}' is not a callable function or lacks a return type", node=self)

            # Check the types of the arguments against the function's parameter types
            if len(self.arguments) != len(func.parameters):
                raise TypeError(f"Function '{self.function.name}' expects {len(func.parameters)} arguments, "
                                f"but {len(self.arguments)} were provided", node=self)

            for arg_node, param_node in zip(self.arguments, func.parameters):
                arg_type = arg_node.get_type(context)
                param_type = param_node.get_type(context)
                if arg_type != param_type:
                    raise TypeError(
                        f"Argument of type {arg_type.__name__} does not match expected type {param_type.__name__} "
                        f"for parameter '{param_node.name}' in function '{self.function.name}'", node=self)

            # Return the function's return type
            return func.return_type
        except Exception as e:
            self.handle_error(e, context)


class ReturnNode(ParserNode):
    """
    A node that represents a return statement.
    - value (ParserNode): The expression that results in the value to be returned.

    Attributes:
        value (ParserNode): The node representing the value being returned.
    """

    def __init__(self, value):
        super().__init__('return')
        self.value = value

    def children(self):
        # Return the value node as it is the only child of a return statement
        if self.value is not None:
            return [self.value]
        return []

    def evaluate(self, context):
        """
        Evaluate the return statement within the given context.
        This evaluates the expression of the return value and handles the control transfer back to the caller.
        """
        # Evaluate the return value expression
        try:
            if self.value is not None:
                return_value = self.value.evaluate(context)
                # Optionally, handle any context or state changes associated with returning
                context.handle_return(return_value)
                return return_value
            # If no value is specified, handle a return with no value (like `return;` in C/C++)
            context.handle_return(None)
            return None
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        """
        Determine and return the type of the return value.
        This is essential for type checking, especially in functions with a specified return type.
        """
        try:
            if self.value is not None:
                return_type = self.value.get_type(context)
                # Optionally, verify that the return type matches the expected function return type
                if context.current_function and context.current_function.return_type != return_type:
                    raise TypeError(f"Return type mismatch: Expected {context.current_function.return_type.__name__}, got {return_type.__name__}")
                return return_type
            # If the function is supposed to return void or similar, handle this case
            return None
        except Exception as e:
            self.handle_error(e, context)



# Data Nodes

class IdentifierNode(ParserNode):
    """
    A node that represents an identifier, which could be a variable name, a function name,
    or any named entity in the language.

    Attributes:
        name (str): The name of the identifier.
    """

    def __init__(self, name):
        super().__init__(name)  # The token might be the identifier itself
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
            raise NameError(f"Identifier '{self.name}' is not declared")
        return context.lookup(self.name)

    def get_type(self, context):
        """
        Determine and return the type of the identifier by looking it up in the context.
        This is essential for type checking and ensuring the identifier is used correctly according to its type.
        """
        if not context.is_declared(self.name):
            raise NameError(f"Identifier '{self.name}' is not declared")
        return context.get_type(self.name)


class PrimitiveDataNode(ParserNode):
    """
    A node that represents primitive data types, serving as a base class for specific types of primitive data.

    Attributes:
        value: The actual data value stored in the node.
    """

    def __init__(self, value):
        super().__init__(str(value))
        self.value = value

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
        raise NotImplementedError("This method should be implemented by subclasses")


class PrimitiveIntNode(PrimitiveDataNode):
    def __init__(self, value):
        super().__init__(value)

    def get_type(self, context):
        # Return the type for integer values
        return int


class PrimitiveFloatNode(PrimitiveDataNode):
    def __init__(self, value):
        super().__init__(value)

    def get_type(self, context):
        # Return the type for float values
        return float


class PrimitiveStringNode(PrimitiveDataNode):
    def __init__(self, value):
        super().__init__(value)

    def get_type(self, context):
        # Return the type for string values
        return str


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
        """
        try:
            # Initialize the variable in the context, possibly with a value
            if self.value is not None:
                value = self.value.evaluate(context)
                context.assign(self.identifier.name, value)
                if self.type_hint:
                    # Type checking between the value and the type hint
                    value_type = self.value.get_type(context)
                    if value_type != self.type_hint:
                        raise TypeError(f"Type mismatch in variable declaration: expected {self.type_hint.__name__}, got {value_type.__name__}")
            else:
                value = None  # Variable declared without an initial value
                if self.type_hint:
                    context.declare_variable(self.identifier.name, self.type_hint)
                else:
                    context.declare_variable(self.identifier.name, type(value))

            # Set the variable type in the context, whether inferred or specified
            context.set_type(self.identifier.name, type(value) if not self.type_hint else self.type_hint)
            return value
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        """
        Determine and return the type of the variable being declared.
        This might be the type hint if provided, or the type of the initial value.
        """
        try:
            if self.type_hint:
                return self.type_hint
            elif self.value:
                return self.value.get_type(context)
            return None  # If no type hint or initial value, the type may be undetermined
        except Exception as e:
            self.handle_error(e, context)


class ArrayNode(ParserNode):
    def __init__(self, elements):
        super().__init__('array')
        self.elements = elements  # List of ParserNodes representing the array elements

    def children(self):
        return self.elements

    def evaluate(self, context):
        try:
            return [element.evaluate(context) for element in self.elements]
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        try:
            if not self.elements:
                return None  # Empty array, type cannot be inferred
            element_type = self.elements[0].get_type(context)
            for element in self.elements:
                if element.get_type(context) != element_type:
                    raise ParserError("Array elements must have the same type", node=self)
            return [element_type]
        except Exception as e:
            self.handle_error(e, context)


# Function Nodes
class FunctionNode(ParserNode):
    """
    A node that represents a function definition.
    - name (str): The name of the function.
    - parameters (list of IdentifierNode): A list of identifiers representing the parameters of the function.
    - body (list of ParserNode): A list of nodes representing the body of the function.

    Attributes:
        name (str): The name of the function.
        parameters (list): The parameters of the function, as a list of IdentifierNodes.
        body (list): The body of the function, as a list of ParserNodes.
    """

    def __init__(self, name, parameters, body, return_type=None):
        super().__init__(name)
        self.name = name
        self.parameters = parameters
        self.body = body
        self.return_type = return_type

    def children(self):
        # Return all parameters and body nodes as children
        return self.parameters + self.body

    def evaluate(self, context: 'Context'):
        """
        Evaluate the function definition within the given context.
        :param context:
        :return:
        """
        try:
            # Create a new context for the function itself
            function_context = Context(parent=context)
            for param in self.parameters:
                function_context.declare_variable(param.name)
            context.store_function(self.name, self, function_context)

            # Perform static analysis for infinite recursion
            self.check_for_infinite_recursion(function_context)
        except Exception as e:
            self.handle_error(e, context)

    def invoke(self, args, context):
        """
        Invoke the function with the provided arguments within the given context.
        :param args:
        :param context:
        :return:
        """
        try:
            context.enter_function_call(self.name)  # Track function call
            if len(args) != len(self.parameters):
                raise ValueError(f"Function '{self.name}' expects {len(self.parameters)} arguments, got {len(args)}")

            local_context = Context(parent=context)
            for param, arg in zip(self.parameters, args):
                local_context.assign(param.name, arg.evaluate(context))

            return_value = None
            for node in self.body:
                result = node.evaluate(local_context)
                if isinstance(node, ReturnNode):
                    return_value = result
                    break

            context.exit_function_call(self.name)  # Untrack function call
            return return_value
        except RecursionError as re:
            raise ParserError(f"Potential infinite recursion detected in function '{self.name}': {str(re)}", node=self)
        except Exception as e:
            self.handle_error(e, context)
            context.exit_function_call(self.name)  # Ensure exit on error

    def check_for_infinite_recursion(self, context):
        """ Perform static analysis to detect potential infinite recursion """
        if not self._has_termination_path(self.body, context):
            raise RecursionError(f"Function '{self.name}' may cause infinite recursion")

    def _has_termination_path(self, nodes, context):
        """ Recursively checks if there's a viable termination path in the function """
        for node in nodes:
            if isinstance(node, ReturnNode):
                return True  # Found a return statement, which is a potential base case
            elif isinstance(node, IfNode):
                then_terminates = self._has_termination_path(node.then_block, context)
                else_terminates = self._has_termination_path(node.else_block, context) if node.else_block else False
                if then_terminates or else_terminates:
                    return True  # If any branch terminates, it's okay
            elif isinstance(node, FunctionCallNode):
                if node.function.name == self.name:
                    continue  # Skip self-recursive calls here
            elif hasattr(node, 'children'):
                if self._has_termination_path(node.children(), context):
                    return True
        return False

    def get_type(self, context):
        """
        Optionally define how to determine the function's return type.
        For example, infer from return statements if the language supports type inference.
        """
        # Placeholder for type determination logic
        return None


class LambdaNode(ParserNode):
    def __init__(self, parameters, body):
        super().__init__('lambda')
        self.parameters = parameters  # List of IdentifierNodes for parameters
        self.body = body              # Body of the lambda, typically a single return expression

    def children(self):
        return self.parameters + [self.body]

    def evaluate(self, context):
        try:
            return lambda *args: self.invoke(args, context)
        except Exception as e:
            self.handle_error(e, context)

    def invoke(self, args, context):
        try:

            local_context = Context(parent=context)
            for param, arg in zip(self.parameters, args):
                local_context.assign(param.name, arg)
            return self.body.evaluate(local_context)
        except Exception as e:
            self.handle_error(e, context)


class ApplyNode(ParserNode):
    def __init__(self, function, arguments):
        super().__init__('apply')
        self.function = function    # FunctionNode or LambdaNode
        self.arguments = arguments  # List of ParserNodes for arguments

    def children(self):
        return [self.function] + self.arguments

    def evaluate(self, context):
        try:
            func = self.function.evaluate(context)
            args = [arg.evaluate(context) for arg in self.arguments]
            return func(*args)
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        try:
            func_type = self.function.get_type(context)
            return func_type
        except Exception as e:
            self.handle_error(e, context)

# class FunctionCallNode(ParserNode):
#     def __init__(self, name, arguments):
#         super().__init__(name)
#         self.arguments = arguments
#
#     def children(self):
#         return self.arguments


class Context:
    MAX_RECURSION_DEPTH = 1000  # Set a limit to prevent stack overflow or infinite recursion

    def __init__(self, parent=None):
        self.parent = parent
        self.symbol_table = {}
        self.function_calls = []
        self.recursion_depth = {}

    def get_type(self, identifier):
        # Lookup identifier in the current context recursively up to the root
        context = self
        while context is not None:
            if identifier in context.symbol_table:
                return context.symbol_table[identifier]
            context = context.parent
        raise Exception("Undefined variable: " + identifier)

    def set_type(self, identifier, type):
        # Set type in the current scope only
        self.symbol_table[identifier] = type

    def declare_variable(self, identifier, type=None):
        if identifier in self.symbol_table:
            raise Exception(f"Variable '{identifier}' already declared in this scope")
        self.symbol_table[identifier] = type

    def is_declared(self, identifier):
        # Check if variable is declared in any accessible scope
        context = self
        while context is not None:
            if identifier in context.symbol_table:
                return True
            context = context.parent
        return False

    def enter_function_call(self, function_name):
        if function_name in self.recursion_depth:
            self.recursion_depth[function_name] += 1
            if self.recursion_depth[function_name] > self.MAX_RECURSION_DEPTH:
                raise RecursionError(f"Exceeded maximum recursion depth in function '{function_name}'")
        else:
            self.recursion_depth[function_name] = 1
        self.function_calls.append(function_name)

    def exit_function_call(self, function_name):
        if function_name in self.function_calls:
            self.function_calls.remove(function_name)
        if function_name in self.recursion_depth:
            self.recursion_depth[function_name] -= 1
            if self.recursion_depth[function_name] == 0:
                del self.recursion_depth[function_name]

    def store_function(self, name, function, function_context):
        self.symbol_table[name] = {
            'function': function,
            'context': function_context
        }

    def lookup_function(self, name):
        if name in self.symbol_table and 'function' in self.symbol_table[name]:
            return self.symbol_table[name]['function']
        raise NameError(f"Function '{name}' is not defined")



class Callable:
    def __init__(self, return_type, arg_types):
        self.return_type = return_type
        self.arg_types = arg_types

    def __call__(self, *args):
        # Perform type checking, argument count checking, etc.
        raise NotImplementedError("This method should be overridden by subclasses")



#Exception Handling

class TryCatchNode(ParserNode):
    def __init__(self, try_block, catch_block, finally_block=None):
        super().__init__('try_catch')
        self.try_block = try_block        # List of ParserNodes for the try block
        self.catch_block = catch_block    # Tuple (exception_type, handler_block)
        self.finally_block = finally_block  # List of ParserNodes for the finally block

    def children(self):
        nodes = self.try_block + [self.catch_block[1]]
        if self.finally_block:
            nodes += self.finally_block
        return nodes

    def evaluate(self, context):
        try:
            for node in self.try_block:
                node.evaluate(context)
        except Exception as e:
            if self.catch_block:
                exception_type, handler_block = self.catch_block
                if isinstance(e, exception_type):
                    catch_context = Context(parent=context)  # New scope for catch block
                    for node in handler_block:
                        node.evaluate(catch_context)
                else:
                    self.handle_error(e, context)
            else:
                self.handle_error(e, context)
        finally:
            if self.finally_block:
                finally_context = Context(parent=context)  # New scope for finally block if needed
                for node in self.finally_block:
                    node.evaluate(finally_context)

    def get_type(self, context):
        try:
            for node in self.try_block:
                node.get_type(context)
            if self.catch_block:
                exception_type, handler_block = self.catch_block
                for node in handler_block:
                    node.get_type(context)
            if self.finally_block:
                for node in self.finally_block:
                    node.get_type(context)
        except Exception as e:
            self.handle_error(e, context)



class ParserError(Exception):
    def __init__(self, message, node=None):
        super().__init__(message)
        self.node = node
        if node:
            # Assuming node has token with line and column or similar identifiers
            self.message = f"Error at line {node.token.line}, column {node.token.column}: {message}"
        else:
            self.message = message

    def __str__(self):
        return self.message



# Create and testt

def test_ast():
    # Construct the nodes based on the provided string
    x_decl = VariableDeclarationNode(IdentifierNode('x'), PrimitiveIntNode(5))
    y_decl = VariableDeclarationNode(IdentifierNode('y'), PrimitiveIntNode(6))
    z_decl = VariableDeclarationNode(IdentifierNode('z'),
                                     BinaryOperationNode('+', IdentifierNode('x'), IdentifierNode('y')))

    condition = BinaryOperationNode('>', IdentifierNode('z'), PrimitiveIntNode(10))
    then_block = ReturnNode(PrimitiveDataNode(True))
    else_block = ReturnNode(PrimitiveDataNode(False))
    if_statement = IfNode(condition, then_block, else_block)

    # Assuming we define a simple function main that encapsulates these operations
    main_function = FunctionNode('main', [], [x_decl, y_decl, z_decl, if_statement])

    # Create a context to track variable types
    context = Context()

    # Walk the AST and print each node type (simplified version)
    def walk_ast(node):
        print(node)
        for child in node.children():
            walk_ast(child)

    # Test walking the AST
    walk_ast(main_function)


if __name__ == "__main__":
    test_ast()


