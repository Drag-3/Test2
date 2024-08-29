import uuid

from ply.lex import LexToken


class ParserNode:
    def __init__(self, token, block_uuid=None):
        self.token = token  # The token representing the node in the syntax tree
        self.block_uuid = block_uuid or str(uuid.uuid4())  # Unique identifier for the block

    def children(self) -> list['ParserNode']:
        # Default implementation returns an empty list, override in derived classes
        return []

    def evaluate(self, context):
        raise NotImplementedError("Each node must implement 'evaluate' method for execution.")

    def get_type(self, context):
        raise NotImplementedError("Each node must implement 'get_type' method for type checking.")

    def handle_error(self, error, context):

        error_message = f"Error in block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)

    def clone(self) -> 'ParserNode':
        # Utility method to clone the current node
        return ParserNode(self.token, self.block_uuid)

    def get_child_by_type(self, node_type) -> 'ParserNode':
        # Utility method to get the first child of a specific type
        for child in self.children():
            if isinstance(child, node_type):
                return child
        return None


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


# Program Structure Nodes
class IfNode(ParserNode):
    """
    A node that represents an if statement.
    - `condition`: The condition to evaluate, which determines which branch to execute.
    - `then_block`: The block of code to execute if the condition is true.
    - `else_block`: The block of code to execute if the condition is false (optional).
    """

    def __init__(self, condition, then_block, else_block=None):
        super().__init__('if')
        self.condition = condition
        self.then_block_uuid = str(uuid.uuid4())  # Unique UUID for then_block
        self.else_block_uuid = str(uuid.uuid4()) if else_block else None  # Unique UUID for else_block
        self.then_block = then_block
        self.else_block = else_block

    def children(self) -> list['ParserNode']:
        # Flatten the lists and return all child nodes, including the else block if it exists
        children = [self.condition] + self.then_block
        if self.else_block:
            children += self.else_block
        return children

    def evaluate(self, context):
        try:
            if self.condition.evaluate(context):
                context.enter_block(self.then_block_uuid)
                for node in self.then_block:
                    node.evaluate(context)
                context.exit_block()
            elif self.else_block:
                context.enter_block(self.else_block_uuid)
                for node in self.else_block:
                    node.evaluate(context)
                context.exit_block()
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        """
        The type of an if statement can be ambiguous if the branches return different types,
        hence we check the types of both branches and raise an error if they don't match.
        If the if statement doesn't return anything explicitly, it can be considered as having 'None' type.
        """
        try:
            then_type = self.then_block[0].get_type(context) if self.then_block else None
            else_type = self.else_block[0].get_type(context) if self.else_block else None
            if else_type and then_type != else_type:
                raise ParserError("Type mismatch between then and else branches", node=self)
            return then_type or else_type
        except Exception as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        block_info = f" in then_block UUID {self.then_block_uuid}"
        if self.else_block and context.get_current_block_uuid() == self.else_block_uuid:
            block_info = f" in else_block UUID {self.else_block_uuid}"
        error_message = f"Error{block_info}: {str(error)}"
        raise ParserError(error_message, node=self)



class WhileNode(ParserNode):
    """
    A node that represents a while loop.
    - `condition`: The condition to evaluate for each loop iteration.
    - `body`: The block of code to execute as long as the condition is true.
    """

    def __init__(self, condition, body):
        super().__init__('while')
        self.condition = condition
        self.body_uuid = str(uuid.uuid4())  # Unique UUID for the loop body
        self.body = body  # List of ParserNodes representing the loop body

    def children(self):
        # Flatten and return both the condition and the body nodes
        return [self.condition] + self.body

    def evaluate(self, context):
        """
        Evaluate the while loop within the given context.
        This method repeatedly evaluates the body as long as the condition evaluates to True.
        """
        try:
            context.enter_block(self.body_uuid)  # Enter the loop body block
            while self.condition.evaluate(context):
                for node in self.body:
                    node.evaluate(context)
            context.exit_block()  # Exit the loop body block
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

    def handle_error(self, error, context):
        error_message = f"Error in while loop body UUID {self.body_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)

class ForNode(ParserNode):
    def __init__(self, initializer, condition, increment, body):
        super().__init__('for')
        self.initializer = initializer  # Typically an AssignmentNode or VariableDeclarationNode
        self.condition = condition      # Expression node that evaluates to a boolean
        self.increment = increment      # UpdateNode or similar for incrementing/decrementing
        self.body_uuid = str(uuid.uuid4())  # Unique UUID for the loop body
        self.body = body                # List of ParserNodes representing the loop body

    def children(self):
        return [self.initializer, self.condition, self.increment] + self.body

    def evaluate(self, context):
        try:
            self.initializer.evaluate(context)
            context.enter_loop(self.body_uuid)  # Enter the loop
            while self.condition.evaluate(context):
                context.enter_block(self.body_uuid)  # Enter the loop body block
                for statement in self.body:
                    statement.evaluate(context)
                context.exit_block()  # Exit the loop body block
                self.increment.evaluate(context)
            context.exit_loop()  # Exit the loop
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        try:
            initializer_type = self.initializer.get_type(context)
            condition_type = self.condition.get_type(context)
            if condition_type != bool:
                raise ParserError("For loop condition must be a boolean", node=self)
            increment_type = self.increment.get_type(context)
            for node in self.body:
                node.get_type(context)
            return None  # For loop itself does not return a value
        except Exception as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in for loop body UUID {self.body_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)



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
        super().__init__('=', block_uuid=str(uuid.uuid4()))  # Generate a unique UUID for this assignment node
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
        super().__init__(operator)  # Generate a unique UUID for this binary operation
        self.operator = operator
        self.left = left
        self.right = right

    def children(self):
        return [self.left, self.right]

    def evaluate(self, context):
        try:
            context.enter_block(self.block_uuid)  # Enter the block for this binary operation

            # Evaluate the left and right operands
            left_value = self.left.evaluate(context)
            right_value = self.right.evaluate(context)

            # Perform the appropriate operation based on the operator
            if self.operator in ['+', '-', '*', '/']:
                result = self.evaluate_arithmetic(left_value, right_value)
            elif self.operator in ['&&', '||']:
                result = self.evaluate_logical(left_value, right_value)
            elif self.operator in ['>>', '|', '++', '<<']:
                result = self.evaluate_stream(left_value, right_value)
            else:
                raise ValueError(f"Unsupported operator: {self.operator}")

            context.exit_block()  # Exit the block after the operation
            return result
        except Exception as e:
            self.handle_error(e, context)

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
        try:
            context.enter_block(self.block_uuid)  # Enter the block for type checking

            left_type = self.left.get_type(context)
            right_type = self.right.get_type(context)

            if left_type != right_type:
                raise TypeError(f"Type mismatch: cannot perform '{self.operator}' between {left_type.__name__} and {right_type.__name__}")

            # Determine the result type based on the operation
            if self.operator == '/' and all(issubclass(t, int) for t in [left_type, right_type]):
                result_type = float
            elif self.operator in ['&&', '||']:
                if left_type == bool and right_type == bool:
                    result_type = bool
                else:
                    raise TypeError("Logical operations require boolean types")
            elif self.operator in ['>>', '|', '++', '<<']:
                result_type = self.determine_stream_type(left_type, right_type)
            else:
                result_type = left_type  # For arithmetic and other operations

            context.exit_block()  # Exit the block after type checking
            return result_type
        except Exception as e:
            self.handle_error(e, context)

    def determine_stream_type(self, left_type, right_type):
        # Placeholder for stream type determination logic
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
        super().__init__(operator, block_uuid=str(uuid.uuid4()))  # Generate a unique UUID for this unary operation
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
        try:
            context.enter_block(self.block_uuid)  # Enter the block for this unary operation

            operand_value = self.operand.evaluate(context)

            if self.operator in ['+', '-']:
                result = self.evaluate_arithmetic(operand_value)
            elif self.operator == '!':
                result = self.evaluate_logical(operand_value)
            elif self.operator == '.to_stream()':
                result = self.evaluate_stream(operand_value)
            else:
                raise ValueError(f"Unsupported unary operator: {self.operator}")

            context.exit_block()  # Exit the block after the operation
            return result
        except Exception as e:
            self.handle_error(e, context)

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
        try:
            context.enter_block(self.block_uuid)  # Enter the block for type checking

            operand_type = self.operand.get_type(context)

            if self.operator in ['+', '-']:
                result_type = operand_type  # Preserves the type of the operand
            elif self.operator == '!':
                if operand_type != bool:
                    raise TypeError("Logical negation requires a boolean type")
                result_type = bool
            elif self.operator == '.to_stream()':
                result_type = StreamType  # Define a type for stream objects if it's a custom class
            else:
                raise TypeError(f"Unsupported unary operator: {self.operator}")

            context.exit_block()  # Exit the block after type checking
            return result_type
        except Exception as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in unary operation block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)


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
        super().__init__('call', block_uuid=str(uuid.uuid4()))  # Generate a unique UUID for this function call
        self.function = function
        self.arguments = arguments

    def children(self):
        # Returns all nodes related to the function and its arguments
        return [self.function] + self.arguments

    def evaluate(self, context):
        try:
            context.enter_block(self.block_uuid)  # Enter the block for this function call

            func = self.function.evaluate(context)
            args_values = [arg.evaluate(context) for arg in self.arguments]
            result = func.invoke(args_values, context)

            context.exit_block()  # Exit the block after the function call
            return result
        except RecursionError as re:
            raise ParserError(f"Infinite recursion detected in function '{self.function.name}': {str(re)}", node=self)
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        try:
            context.enter_block(self.block_uuid)  # Enter the block for type checking

            # Resolve the function from the context
            func = self.function.evaluate(context)

            # Check if func is actually a function and has a return type
            if not hasattr(func, 'return_type') or func.return_type is None:
                # Infer the return type from the function body if not explicitly provided
                inferred_return_type = self.infer_return_type(func, context)
                func.return_type = inferred_return_type  # Set the inferred type as the function's return type
            else:
                inferred_return_type = func.return_type

            # Check the types of the arguments against the function's parameter types
            if len(self.arguments) != len(func.parameters):
                raise ParserError(f"Function '{self.function.name}' expects {len(func.parameters)} arguments, "
                                f"but {len(self.arguments)} were provided", node=self)

            for arg_node, param_node in zip(self.arguments, func.parameters):
                arg_type = arg_node.get_type(context)
                param_type = param_node.get_type(context)

                # If the parameter type is not explicitly stated, infer it
                if param_type is None:
                    param_node.type_hint = arg_type
                elif arg_type != param_type:
                    raise ParserError(
                        f"Argument of type {arg_type.__name__} does not match expected type {param_type.__name__} "
                        f"for parameter '{param_node.name}' in function '{self.function.name}'", node=self)

            context.exit_block()  # Exit the block after type checking
            # Return the function's inferred or explicit return type
            return inferred_return_type
        except Exception as e:
            self.handle_error(e, context)

    def infer_return_type(self, func, context):
        """
        Infer the return type of the function by analyzing the function's body.
        """
        try:
            # Analyze the function's body to infer the return type
            return_types = []
            for node in func.body:
                if isinstance(node, ReturnNode):
                    return_types.append(node.get_type(context))

            # If all return types are consistent, return the common type
            if len(set(return_types)) == 1:
                return return_types[0]
            else:
                raise TypeError(f"Function '{self.function.name}' has inconsistent return types", node=self)
        except Exception as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in function call block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)


class ReturnNode(ParserNode):
    """
    A node that represents a return statement.
    - value (ParserNode): The expression that results in the value to be returned.

    Attributes:
        value (ParserNode): The node representing the value being returned.
    """

    def __init__(self, value):
        super().__init__('return', block_uuid=str(uuid.uuid4()))  # Generate a unique UUID for this return statement
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
        try:
            context.enter_block(self.block_uuid)  # Enter the block for this return statement

            # Evaluate the return value expression
            if self.value is not None:
                return_value = self.value.evaluate(context)
                context.handle_return(return_value)
                context.exit_block()  # Exit the block after evaluating the return value
                return return_value
            else:
                context.handle_return(None)
                context.exit_block()  # Exit the block even if there's no return value
                return None
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        """
        Determine and return the type of the return value.
        This is essential for type checking, especially in functions with a specified return type.
        """
        try:
            context.enter_block(self.block_uuid)  # Enter the block for type checking

            if self.value is not None:
                return_type = self.value.get_type(context)

                # If the function has a return type defined, ensure compatibility
                if context.current_function:
                    expected_return_type = context.current_function.return_type
                    if expected_return_type is None:
                        # If no return type is specified, infer it from the current return statement
                        context.current_function.return_type = return_type
                    elif expected_return_type != return_type:
                        raise TypeError(
                            f"Return type mismatch: Expected {expected_return_type.__name__}, got {return_type.__name__}")

                context.exit_block()  # Exit the block after type checking
                return return_type
            else:
                context.exit_block()  # Exit the block when there's no return value to type check
                return None
        except Exception as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in return statement block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)



# Data Nodes

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

    def get_type(self, context):
        """
        Determine and return the type of the identifier by looking it up in the context.
        This is essential for type checking and ensuring the identifier is used correctly according to its type.
        """
        try:
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

class PrimitiveDataNode(ParserNode):
    """
    A node that represents primitive data types, serving as a base class for specific types of primitive data.

    Attributes:
        value: The actual data value stored in the node.
    """

    def __init__(self, value):
        super().__init__(str(value), block_uuid=str(uuid.uuid4()))  # Generate a unique UUID for this primitive data node
        self.value = value

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
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        """
        Determine and return the type of the primitive data.
        This method must be overridden in subclasses to return the correct type.
        """
        raise NotImplementedError("This method should be implemented by subclasses")

    def handle_error(self, error, context):
        error_message = f"Error in primitive data node with block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)


class PrimitiveIntNode(PrimitiveDataNode):
    def __init__(self, value):
        super().__init__(value)

    def get_type(self, context):
        try:
            context.enter_block(self.block_uuid)  # Enter the block for type checking
            result_type = int  # Return the type for integer values
            context.exit_block()  # Exit the block after type checking
            return result_type
        except Exception as e:
            self.handle_error(e, context)


class PrimitiveFloatNode(PrimitiveDataNode):
    def __init__(self, value):
        super().__init__(value)

    def get_type(self, context):
        try:
            context.enter_block(self.block_uuid)  # Enter the block for type checking
            result_type = float  # Return the type for float values
            context.exit_block()  # Exit the block after type checking
            return result_type
        except Exception as e:
            self.handle_error(e, context)


class PrimitiveStringNode(PrimitiveDataNode):
    def __init__(self, value):
        super().__init__(value)

    def get_type(self, context):
        try:
            context.enter_block(self.block_uuid)  # Enter the block for type checking
            result_type = str  # Return the type for string values
            context.exit_block()  # Exit the block after type checking
            return result_type
        except Exception as e:
            self.handle_error(e, context)


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
        super().__init__('var_decl',
                         block_uuid=str(uuid.uuid4()))  # Generate a unique UUID for this variable declaration
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


class ArrayNode(ParserNode):
    def __init__(self, elements):
        super().__init__('array', block_uuid=str(uuid.uuid4()))  # Generate a unique UUID for this array node
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
        except Exception as e:
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
        except Exception as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in array node with block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)


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
        return_type (type, optional): The return type of the function if explicitly specified.
    """

    def __init__(self, name, parameters, body, return_type=None):
        super().__init__(name, block_uuid=str(uuid.uuid4()))  # Generate a unique UUID for this function node
        self.name = name
        self.parameters = parameters
        self.body = body
        self.return_type = return_type

    def children(self):
        # Return all parameters and body nodes as children
        return self.parameters + self.body

    def evaluate(self, context):
        """
        Evaluate the function definition within the given context.
        This registers the function in the context.
        """
        try:
            context.enter_block(self.block_uuid)  # Enter the block for this function definition

            # Create a new context for the function itself
            function_context = Context(parent=context)
            for param in self.parameters:
                function_context.declare_variable(param.name)
            context.store_function(self.name, self, function_context)

            # Perform static analysis for infinite recursion
            self.check_for_infinite_recursion(function_context)

            context.exit_block()  # Exit the block after evaluating the function definition
        except Exception as e:
            self.handle_error(e, context)

    def invoke(self, args, context):
        """
        Invoke the function with the provided arguments within the given context.
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
        Determine the function's return type.
        If not explicitly provided, infer from return statements.
        """
        try:
            context.enter_block(self.block_uuid)  # Enter the block for type inference

            if self.return_type:
                result_type = self.return_type  # Use the explicitly provided return type
            else:
                result_type = None
                for node in self.body:
                    if isinstance(node, ReturnNode):
                        inferred_type = node.get_type(context)
                        if result_type is None:
                            result_type = inferred_type
                        elif result_type != inferred_type:
                            raise TypeError(f"Conflicting return types in function '{self.name}': "
                                            f"{result_type} and {inferred_type}")

            context.exit_block()  # Exit the block after type inference
            return result_type
        except Exception as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in function '{self.name}' with block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)


class LambdaNode(ParserNode):
    def __init__(self, parameters, body):
        super().__init__('lambda', block_uuid=str(uuid.uuid4()))  # Generate a unique UUID for this lambda node
        self.parameters = parameters  # List of IdentifierNodes for parameters
        self.body = body  # Body of the lambda, typically a single return expression

    def children(self):
        return self.parameters + [self.body]

    def evaluate(self, context):
        try:
            context.enter_block(self.block_uuid)  # Enter the block for this lambda node
            return lambda *args: self.invoke(args, context)
        except Exception as e:
            self.handle_error(e, context)
        finally:
            context.exit_block()  # Ensure we exit the block after evaluation

    def invoke(self, args, context):
        try:
            local_context = Context(parent=context)
            for param, arg in zip(self.parameters, args):
                local_context.assign(param.name, arg)
            return self.body.evaluate(local_context)
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        try:
            context.enter_block(self.block_uuid)  # Enter the block for type inference
            return_type = self.body.get_type(context)
            context.exit_block()  # Exit the block after type inference
            return return_type
        except Exception as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in lambda function with block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)


class ApplyNode(ParserNode):
    def __init__(self, function, arguments):
        super().__init__('apply', block_uuid=str(uuid.uuid4()))  # Generate a unique UUID for this apply node
        self.function = function  # FunctionNode or LambdaNode
        self.arguments = arguments  # List of ParserNodes for arguments

    def children(self):
        return [self.function] + self.arguments

    def evaluate(self, context):
        try:
            context.enter_block(self.block_uuid)  # Enter the block for this apply node
            func = self.function.evaluate(context)
            args = [arg.evaluate(context) for arg in self.arguments]
            return func(*args)
        except Exception as e:
            self.handle_error(e, context)
        finally:
            context.exit_block()  # Ensure we exit the block after evaluation

    def get_type(self, context):
        try:
            context.enter_block(self.block_uuid)  # Enter the block for type inference
            func_type = self.function.get_type(context)
            context.exit_block()  # Exit the block after type inference
            return func_type
        except Exception as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in apply operation with block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)

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
        self.global_symbol_table = self._get_global_symbol_table() if parent else {}
        self.local_symbol_tables = [{}]  # Ensure at least one local scope
        self.function_calls = []
        self.blocks_stack = []  # Stack to manage block UUIDs
        self.recursion_depth = {}
        self.current_block_uuid = None
        self.call_stack = []  # Stack to maintain function call trace
        self.loop_stack = []  # Stack to manage loop states
    def _get_global_symbol_table(self):
        if self.parent:
            return self.parent._get_global_symbol_table()
        return self.global_symbol_table

    # Variable and Type Management
    def get_type(self, identifier):
        context = self
        while context is not None:
            for symbol_table in reversed(context.local_symbol_tables):
                if identifier in symbol_table:
                    return symbol_table[identifier]
            context = context.parent

        if identifier in self.global_symbol_table:
            return self.global_symbol_table[identifier]

        raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared in the current scope.")

    def set_type(self, identifier, t, global_scope=False):
        # Set type in the appropriate scope (global or local)
        if global_scope:
            self.global_symbol_table[identifier] = t
        else:
            self.local_symbol_tables[-1][identifier] = t

    def declare_variable(self, identifier, t=None):
        if not self.local_symbol_tables or identifier in self.local_symbol_tables[-1]:
            raise Exception(f"Variable '{identifier}' already declared in this scope or no scope available.")

        # Ensure variable is not declared in any parent context to prevent shadowing in the same block
        if self.parent:
            if self.parent.is_declared_in_current_scope(identifier):
                raise Exception(f"Variable '{identifier}' already declared in an outer scope")

        # Declare the variable in the current local scope
        self.local_symbol_tables[-1][identifier] = t

    def is_declared(self, identifier):
        # Check if variable is declared in any accessible scope
        try:
            self.get_type(identifier)
            return True
        except VariableNotDeclaredError:
            return False

    def assign(self, identifier, value):
        context = self
        while context is not None:
            if context.local_symbol_tables and identifier in context.local_symbol_tables[-1]:
                context.local_symbol_tables[-1][identifier] = value
                return
            context = context.parent

        # Then, try to assign in the global scope
        if identifier in self.global_symbol_table:
            self.global_symbol_table[identifier] = value
        else:
            raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared in the current scope.")

    def lookup(self, identifier):
        # Lookup identifier first in local scopes, then global
        for symbol_table in reversed(self.local_symbol_tables):
            if identifier in symbol_table:
                return symbol_table[identifier]
        if identifier in self.global_symbol_table:
            return self.global_symbol_table[identifier]
        if self.parent:
            return self.parent.lookup(identifier)
        raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared in the current scope.")


    # Block Management
    def enter_block(self, block_uuid):
        self.blocks_stack.append(self.current_block_uuid)
        self.current_block_uuid = block_uuid

    def exit_block(self):
        self.current_block_uuid = self.blocks_stack.pop()
        self._clean_up_variables()

    def get_current_block_uuid(self):
        return self.current_block_uuid

    def _clean_up_variables(self):
        # Clean up variables declared in the current block
        if self.local_symbol_tables:
            self.local_symbol_tables.pop()

    # Scope Management
    def enter_scope(self):
        self.local_symbol_tables.append({})

    def exit_scope(self):
        self.local_symbol_tables.pop()

    # Function Call Management
    def enter_function_call(self, function_name, params=None):
        if function_name in self.recursion_depth:
            self.recursion_depth[function_name] += 1
            if self.recursion_depth[function_name] > self.MAX_RECURSION_DEPTH:
                raise RecursionError(f"Exceeded maximum recursion depth in function '{function_name}'")
        else:
            self.recursion_depth[function_name] = 1

        new_context = Context(parent=self)
        if params:
            for param_name, param_value in params.items():
                new_context.declare_variable(param_name, param_value)
        new_context.enter_scope()
        new_context.function_calls.append(function_name)
        new_context.call_stack.append(function_name)
        self.enter_block(str(uuid.uuid4()))  # Assign a new block UUID for the function scope
        return new_context

    def exit_function_call(self, function_name):
        if function_name in self.call_stack:
            self.call_stack.pop()
        if function_name in self.recursion_depth:
            self.recursion_depth[function_name] -= 1
            if self.recursion_depth[function_name] == 0:
                del self.recursion_depth[function_name]
        self.exit_scope()
        self.exit_block()

    def store_function(self, name, function, function_context):
        self.global_symbol_table[name] = {
            'function': function,
            'context': function_context
        }

    def lookup_function(self, name):
        if name in self.global_symbol_table and 'function' in self.global_symbol_table[name]:
            return self.global_symbol_table[name]['function']
        raise FunctionNotFoundError(f"Function '{name}' is not defined in the current scope.")

    def handle_return(self, value):
        # Store the return value in the context if needed
        self.return_value = value

    # Loop Management
    def enter_loop(self, loop_uuid):
        self.loop_stack.append(loop_uuid)

    def exit_loop(self):
        self.loop_stack.pop()

    def get_current_loop(self):
        return self.loop_stack[-1] if self.loop_stack else None

    # Debugging and Tracing
    def dump_state(self):
        print("Current Block UUID:", self.current_block_uuid)
        print("Current Symbol Table:", self.local_symbol_tables[-1])
        print("Global Symbol Table:", self.global_symbol_table)
        print("Function Calls:", self.function_calls)
        print("Call Stack:", self.call_stack)
        print("Block Stack:", self.blocks_stack)
        print("Loop Stack:", self.loop_stack)
        print("Recursion Depth:", self.recursion_depth)

    # Cloning Context
    def clone(self):
        new_context = Context(parent=self.parent)
        new_context.global_symbol_table = self.global_symbol_table.copy()
        new_context.local_symbol_tables = [table.copy() for table in self.local_symbol_tables]
        new_context.function_calls = self.function_calls.copy()
        new_context.blocks_stack = self.blocks_stack.copy()
        new_context.recursion_depth = self.recursion_depth.copy()
        new_context.current_block_uuid = self.current_block_uuid
        new_context.call_stack = self.call_stack.copy()
        new_context.loop_stack = self.loop_stack.copy()
        return new_context

    def reset(self):
        self.local_symbol_tables = [{}]
        self.function_calls = []
        self.blocks_stack = []
        self.recursion_depth = {}
        self.current_block_uuid = None
        self.call_stack = []
        self.loop_stack = []


class Callable:
    def __init__(self, return_type=None, arg_types=None):
        """
        Initialize the callable object.
        :param return_type: The expected return type of the callable (optional).
        :param arg_types: A list of expected argument types (optional).
        """
        self.return_type = return_type  # Expected return type
        self.arg_types = arg_types or []  # List of expected argument types

    def __call__(self, *args):
        """
        Invoke the callable object with the provided arguments.
        :param args: Arguments passed to the callable.
        :return: The result of the callable execution.
        """
        self._check_argument_count(args)
        self._check_argument_types(args)
        result = self.invoke(*args)
        self._check_return_type(result)
        return result

    def invoke(self, *args):
        """
        Subclasses should implement this method to define the callable's behavior.
        :param args: Arguments passed to the callable.
        :return: The result of the callable execution.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def _check_argument_count(self, args):
        """
        Check if the number of arguments passed matches the expected count.
        :param args: Arguments passed to the callable.
        :raises TypeError: If the argument count does not match.
        """
        if len(args) != len(self.arg_types):
            raise TypeError(
                f"Expected {len(self.arg_types)} arguments, but got {len(args)}"
            )

    def _check_argument_types(self, args):
        """
        Check if the types of the arguments match the expected types.
        :param args: Arguments passed to the callable.
        :raises TypeError: If an argument type does not match the expected type.
        """
        for i, (arg, expected_type) in enumerate(zip(args, self.arg_types)):
            if not isinstance(arg, expected_type):
                raise TypeError(
                    f"Argument {i} expected to be of type {expected_type.__name__}, but got {type(arg).__name__}"
                )

    def _check_return_type(self, result):
        """
        Check if the return type of the callable matches the expected return type.
        :param result: The result returned by the callable.
        :raises TypeError: If the return type does not match the expected return type.
        """
        if self.return_type and not isinstance(result, self.return_type):
            raise TypeError(
                f"Expected return type {self.return_type.__name__}, but got {type(result).__name__}"
            )

    def __str__(self):
        return f"Callable(return_type={self.return_type}, arg_types={self.arg_types})"

    def __repr__(self):
        return self.__str__()




#Exception Handling

class TryCatchNode(ParserNode):
    def __init__(self, try_block, catch_block, finally_block=None):
        super().__init__('try_catch')
        self.try_block = try_block        # List of ParserNodes for the try block
        self.catch_block = catch_block    # Tuple (exception_type, handler_block)
        self.finally_block = finally_block  # List of ParserNodes for the finally block
        self.block_uuid = str(uuid.uuid4())  # Unique identifier for this block

    def children(self):
        nodes = self.try_block + [self.catch_block[1]]
        if self.finally_block:
            nodes += self.finally_block
        return nodes

    def evaluate(self, context):
        context.enter_block(self.block_uuid)
        try:
            for node in self.try_block:
                node.evaluate(context)
        except Exception as e:
            if self.catch_block:
                exception_type, handler_block = self.catch_block
                if isinstance(e, exception_type):
                    catch_context = context.clone()
                    context.enter_block(str(uuid.uuid4()))  # New block UUID for the catch block
                    for node in handler_block:
                        node.evaluate(catch_context)
                    context.exit_block()
                else:
                    self.handle_error(e, context)
            else:
                self.handle_error(e, context)
        finally:
            if self.finally_block:
                finally_context = context.clone()
                context.enter_block(str(uuid.uuid4()))  # New block UUID for the finally block
                for node in self.finally_block:
                    node.evaluate(finally_context)
                context.exit_block()
        context.exit_block()

    def get_type(self, context):
        try:
            context.enter_block(self.block_uuid)
            for node in self.try_block:
                node.get_type(context)
            if self.catch_block:
                exception_type, handler_block = self.catch_block
                context.enter_block(str(uuid.uuid4()))  # New block UUID for the catch block
                for node in handler_block:
                    node.get_type(context)
                context.exit_block()
            if self.finally_block:
                context.enter_block(str(uuid.uuid4()))  # New block UUID for the finally block
                for node in self.finally_block:
                    node.get_type(context)
                context.exit_block()
        except Exception as e:
            self.handle_error(e, context)
        finally:
            context.exit_block()



class ParserError(Exception):
    def __init__(self, message, node=None):
        super().__init__(message)
        self.node = node
        if node:
            # Assuming node has token with line and column or similar identifiers
            self.message = f"Error at line : {message}"
        else:
            self.message = message

    def __str__(self):
        return self.message

class VariableNotDeclaredError(ParserError):
    def __init__(self, message):
        super().__init__(message)


class FunctionNotFoundError(ParserError):
    def __init__(self, message):
        super().__init__(message)


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


