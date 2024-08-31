from .exceptions import ReturnException

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


class CallableFunction(Callable):
    def __init__(self, name, parameters, body, return_type=None):
        super().__init__(return_type=return_type, arg_types=[])
        self.name = name
        self.parameters = parameters
        self.body = body

    def invoke(self, *args, context):
        local_context = context.enter_function_call(self.name)

        # Declare parameters without types initially
        for param in self.parameters:
            local_context.declare_variable(param.name)

        # Bind parameters to arguments and infer/update types
        for param, arg in zip(self.parameters, args):
            param_type = param.get_type(local_context) if param.get_type(local_context) else type(arg)
            local_context.assign(param.name, arg)
            local_context.set_type(param.name, param_type)

        # Execute the function body
        result = None
        try:
            for node in self.body:
                node.evaluate(local_context)
        except ReturnException as re:
            result = re.value

        context.exit_function_call(self.name)
        return result