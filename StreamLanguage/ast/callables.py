from StreamLanguage.ast.exceptions import ReturnException, SLTypeError
from StreamLanguage.exceptions import SLException


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
            raise SLTypeError(
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
                raise SLTypeError(
                    f"Argument {i} expected to be of type {expected_type.__name__}, but got {type(arg).__name__}"
                )

    def _check_return_type(self, result):
        """
        Check if the return type of the callable matches the expected return type.
        :param result: The result returned by the callable.
        :raises TypeError: If the return type does not match the expected return type.
        """
        if self.return_type and not isinstance(result, self.return_type):
            raise SLTypeError(
                f"Expected return type {self.return_type.__name__}, but got {type(result).__name__}"
            )

    def __str__(self):
        return f"Callable(return_type={self.return_type}, arg_types={self.arg_types})"

    def __repr__(self):
        return self.__str__()


class CallableFunction(Callable):
    def __init__(self, name, parameters, body, return_type=None):
        super().__init__(return_type=return_type, arg_types=[])
        self.name = name
        self.parameters = parameters
        self.body = body

    def invoke(self, *args, context):
        """
        Invoke the function with the provided arguments within the given context.
        """
        f_ctx = None
        try:
            f_ctx = context.enter_function_call(self, args)  # Set up the function call context

            return_value = None
            try:
                for node in self.body:
                    node.evaluate(f_ctx)
            except ReturnException as re:
                return_value = f_ctx.handle_return(re.value)

            context.exit_function_call(f_ctx)  # Untrack function call
            return return_value
        except SLException as e:
            context.exit_function_call(f_ctx)  # Ensure proper cleanup on error
            self.handle_error(e, context)

    def handle_error(self, e, context):
        error_message = f"Error in function '{self.name}': {str(e)}"
        raise SLException(error_message)
