from StreamLanguage.ast.nodes.base import ParserNode
from StreamLanguage.ast.nodes.flow_control import IfNode
from StreamLanguage.ast.exceptions import ParserError, FunctionNotFoundError, SLRecursionError, ReturnException, SLTypeError
from StreamLanguage.exceptions import SLException
from StreamLanguage.ast.symbol_table import SymbolTableEntry
from StreamLanguage.ast.callables import CallableFunction
from StreamLanguage.ast.block_types import BlockType
import uuid


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

    BLOCKTYPE = BlockType.FUNCTION
    def __init__(self, name, parameters, body, return_type=None):
        super().__init__(name)  # Generate a unique UUID for this function node
        self.name = name
        self.parameters = parameters
        self.body = body
        self.return_type = return_type

    def children(self):
        # Return all parameters and body nodes as children
        return self.parameters + self.body

    def evaluate(self, context):
        callable_function = CallableFunction(self.name, self.parameters, self.body, self.return_type)
        context.declare_function(self.name, callable_function, self.parameters, self.return_type, global_scope=False)


    def check_for_infinite_recursion(self, context):
        """ Perform static analysis to detect potential infinite recursion. """
        visited = set()  # To keep track of visited nodes and avoid re-checking them
        if not self._has_termination_path(self.body, context, visited):
            raise SLRecursionError(f"Function '{self.name}' may cause infinite recursion")


    def _has_termination_path(self, nodes, context, visited):
        """ Recursively checks if there's a viable termination path in the function. """
        for node in nodes:
            if node in visited:
                continue  # Skip already checked nodes to prevent unnecessary reevaluation
            visited.add(node)

            if isinstance(node, ReturnNode):
                return True
            elif isinstance(node, IfNode):
                then_terminates = self._has_termination_path(node.then_block, context, visited)
                else_terminates = self._has_termination_path(node.else_block, context, visited) if node.else_block else False
                if then_terminates or else_terminates:
                    return True
            elif isinstance(node, FunctionCallNode):
                # Check for self-recursion directly or indirectly via other functions
                if node.function.name == self.name or context.is_recursive_call(node.function.name, self.name):
                    continue
            elif hasattr(node, 'children'):
                if self._has_termination_path(node.children(), context, visited):
                    return True
        return False

    def get_type(self, context):
        if self.return_type:
            return self.return_type

        return self.infer_return_type(context)

    def infer_return_type(self, context):
        """
        Infer the return type by analyzing the return statements within the function body.
        Assumes that all return paths return the same type or throws a type inconsistency error.
        """
        inferred_types = set()
        for node in self.body:
            if isinstance(node, ReturnNode):
                inferred_types.add(node.get_type(context))

        if len(inferred_types) == 1:
            return next(iter(inferred_types))  # Return the single inferred type
        elif not inferred_types:
            return None  # No return statements imply a possible 'void' type or equivalent
        else:
            raise SLTypeError(f"Function '{self.name}' has inconsistent return types")


    def handle_error(self, error, context):
        error_message = f"Error in function '{self.name}' with block UUID {self.block_uuid}: {str(error)}"
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
            context.enter_block(self.block_uuid, BlockType.FUNCTION)  # Enter the block for this function call

            # Lookup the function in the symbol table
            func_info = context.lookup_function(self.function.name)
            func = func_info.get('callable')
            args_values = [arg.evaluate(context) for arg in self.arguments]
            result = func.invoke(*args_values, context=context)

            context.exit_block()  # Exit the block after the function call
            return result
        except SLRecursionError as re:
            raise ParserError(f"Infinite recursion detected in function '{self.function.name}': {str(re)}", node=self)
        except SLException as e:
            context.exit_block()
            self.handle_error(e, context)

    def get_type(self, context):
        function_callable = context.lookup_function(self.function.name)
        if function_callable is None:
            raise FunctionNotFoundError(f"Function '{self.function.name}' not found")

        # Match argument types with parameter types
        expected_types = [param.get_type(context) for param in function_callable.parameters]
        given_types = [arg.get_type(context) for arg in self.arguments]

        if len(expected_types) != len(given_types):
            raise SLTypeError(f"Function '{self.function.name}' called with incorrect number of arguments")

        for expected, given in zip(expected_types, given_types):
            if expected != given:
                raise SLTypeError(
                    f"Type mismatch in function call '{self.function.name}': expected {expected}, got {given}")

        return function_callable.get_type(context)  # This should invoke FunctionNode.get_type

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
                raise ReturnException(return_value)  # Raise a signal to return the value
            else:
                context.handle_return(None)
                context.exit_block()  # Exit the block even if there's no return value
                return None
        except ReturnException as re:
            raise re  # Propagate the return signal to the caller
        except SLException as e:
            self.handle_error(e, context)

    def get_type(self, context):
        """
        Determine and return the type of the return value.
        If the function is supposed to return a specific type, this method ensures that
        the type of the value node matches the expected return type.
        """
        if self.value is None:
            return None

        return_type = self.value.get_type(context)

        if context.current_function and context.current_function.return_type:
            if return_type != context.current_function.return_type:
                raise SLTypeError(f"Type mismatch: Function expected to return {context.current_function.return_type}, but got {return_type}")

        return return_type

    def handle_error(self, error, context):
        error_message = f"Error in return statement block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)


class LambdaNode(ParserNode):
    def __init__(self, parameters, body):
        super().__init__('lambda')
        self.parameters = parameters
        self.body = body

    def evaluate(self, context):
        # Returns a callable that captures the current context for later execution
        def lambda_function(*args):
            lambda_context = context.enter_function_call(self, args)
            try:
                result = None
                for node in self.body:
                    result = node.evaluate(lambda_context)
                return result
            finally:
                context.exit_function_call(lambda_context)
        return lambda_function

    def get_type(self, context):
        # Type of lambda should be inferred from the return type of its body
        if isinstance(self.body, list):
            return self.body[-1].get_type(context)
        return self.body.get_type(context)



class ApplyNode(ParserNode):
    def __init__(self, function, arguments):
        super().__init__('apply')
        self.function = function
        self.arguments = arguments

    def evaluate(self, context):
        func = self.function.evaluate(context)
        args = [arg.evaluate(context) for arg in self.arguments]
        return func(*args)  # Call the function with arguments

    def get_type(self, context):
        # This should reflect the return type of the function being applied
        func_type = self.function.get_type(context)
        # Validate the argument types if the function specifies expected types
        expected_types = [param.get_type(context) for param in self.function.parameters]
        given_types = [arg.get_type(context) for arg in self.arguments]
        for expected, given in zip(expected_types, given_types):
            if expected != given:
                raise SLTypeError(f"Type mismatch in function call '{self.function}': expected {expected}, got {given}")
        return func_type

