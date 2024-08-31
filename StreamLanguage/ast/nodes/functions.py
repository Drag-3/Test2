from.base import ParserNode
from .flow_control import IfNode
from ..exceptions import ParserError, FunctionNotFoundError, SLRecursionError, ReturnException
from ..symbol_table import SymbolTableEntry
from ..callables import CallableFunction
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
        """
        Evaluate the function definition within the given context.
        Store the function in the global symbol table.
        """
        try:
            # Store the function as a Callable in the symbol table
            callable_function = CallableFunction(self.name, self.parameters, self.body, self.return_type)
            context.declare_function(self.name, callable_function, global_scope=False)
        except Exception as e:
            self.handle_error(e, context)

    def invoke(self, *args, context):
        """
        Invoke the function with the provided arguments within the given context.
        """
        try:
            context.enter_function_call(self.name)  # Track function call
            context.enter_block(self.block_uuid)

            # Create a new scope for function parameters
            context.enter_scope()
            for param, arg in zip(self.parameters, args):
                param_type = param.get_type(context)
                context.symbol_table.store(param.name, SymbolTableEntry(value=arg.evaluate(context), entry_type=param_type))

            return_value = None
            try:
                for node in self.body:
                    node.evaluate(context)
            except ReturnException as re:
                return_value = re.value

            context.exit_scope()
            context.exit_block()
            context.exit_function_call(self.name)  # Untrack function call
            return return_value
        except Exception as e:
            context.exit_scope()
            context.exit_block()
            context.exit_function_call(self.name)  # Ensure proper cleanup on error
            self.handle_error(e, context)

    def check_for_infinite_recursion(self, context):
        """ Perform static analysis to detect potential infinite recursion """
        if not self._has_termination_path(self.body, context):
            raise SLRecursionError(f"Function '{self.name}' may cause infinite recursion")

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
        try:
            context.enter_block(self.block_uuid)  # Enter the block for type inference

            if self.return_type:
                result_type = self.return_type  # Use the explicitly provided return type
            else:
                result_type = self.infer_return_type(context)

            context.exit_block()  # Exit the block after type inference
            return result_type
        except Exception as e:
            self.handle_error(e, context)

    def infer_return_type(self, context):
        """
        Infer the return type by analyzing the function's body.
        """
        return_types = [node.get_type(context) for node in self.body if isinstance(node, ReturnNode)]
        if len(set(return_types)) == 1:
            return return_types[0]
        elif return_types:
            raise TypeError(f"Function '{self.name}' has inconsistent return types")
        return None

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
            context.enter_block(self.block_uuid)  # Enter the block for this function call

            # Lookup the function in the symbol table
            func = context.lookup_function(self.function.name)

            args_values = [arg.evaluate(context) for arg in self.arguments]
            result = func.invoke(*args_values, context=context)

            context.exit_block()  # Exit the block after the function call
            return result
        except SLRecursionError as re:
            raise ParserError(f"Infinite recursion detected in function '{self.function.name}': {str(re)}", node=self)
        except Exception as e:
            context.exit_block()
            self.handle_error(e, context)

    def get_type(self, context):
        try:
            context.enter_block(self.block_uuid)  # Enter the block for type checking

            # Lookup the function in the symbol table
            func_entry = context.lookup(self.function.name)
            if not func_entry or func_entry.entry_type != 'function':
                raise FunctionNotFoundError(f"Function '{self.function.name}' is not defined")

            func = func_entry.value
            return_type = func.get_type(context)

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
            return return_type
        except Exception as e:
            context.exit_block()
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
                raise ReturnException(return_value)  # Raise a signal to return the value
            else:
                context.handle_return(None)
                context.exit_block()  # Exit the block even if there's no return value
                return None
        except ReturnException as re:
            raise re  # Propagate the return signal to the caller
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


class LambdaNode(ParserNode):
    def __init__(self, parameters, body):
        super().__init__('lambda', block_uuid=str(uuid.uuid4()))
        self.parameters = parameters  # List of IdentifierNodes for parameters
        self.body = body              # Body of the lambda, typically a single return expression

    def children(self):
        return self.parameters + [self.body]

    def evaluate(self, context):
        try:
            return lambda *args: self.invoke(args, context)
        except Exception as e:
            self.handle_error(e, context)

    def invoke(self, *args, context):
        try:
            context.enter_scope()
            context.enter_block(self.block_uuid)

            # Bind parameters to arguments in a new scope
            for param, arg in zip(self.parameters, args):
                # If the parameter type is not yet set, infer it from the argument
                if not context.is_declared(param.name):
                    inferred_type = type(arg)
                    context.declare_variable(param.name, t=inferred_type, value=arg)
                else:
                    context.assign(param.name, arg)

            result = self.body.evaluate(context)

            context.exit_block()
            context.exit_scope()
            return result
        except Exception as e:
            context.exit_block()
            context.exit_scope()
            self.handle_error(e, context)

    def get_type(self, context):
        """
        Infer the type of the lambda expression based on the return type of its body.
        """
        try:
            context.enter_scope()
            context.enter_block(self.block_uuid)

            return_type = self.body.get_type(context)

            context.exit_block()
            context.exit_scope()
            return return_type
        except Exception as e:
            context.exit_block()
            context.exit_scope()
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

            # Ensure that the function's return type is consistent
            if isinstance(func_type, list) and len(func_type) == len(self.arguments):
                for arg, expected_type in zip(self.arguments, func_type):
                    arg_type = arg.get_type(context)
                    if arg_type != expected_type:
                        raise TypeError(f"Argument type mismatch: expected {expected_type}, got {arg_type}")

            context.exit_block()  # Exit the block after type inference
            return func_type
        except Exception as e:
            self.handle_error(e, context)


    def handle_error(self, error, context):
        error_message = f"Error in apply operation with block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)