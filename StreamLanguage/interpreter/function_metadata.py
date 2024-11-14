from StreamLanguage.ast.exceptions import VariableRedeclaredError, FunctionNotFoundError


class FunctionOverload:
    def __init__(self, parameters, return_type, body):
        if parameters is None:
            parameters = []

        self.parameters = parameters
        self.return_type = return_type
        self.implementation = body

    def matches(self, argument_types):
        """
        Check if the overload matches the provided argument sl_types based on parameter count.

        :param argument_types: List of argument sl_types.
        :return: True if matches, False otherwise.
        """
        return len(self.parameters) == len(argument_types)


    def __repr__(self):
        return f"FunctionOverload(parameters={self.parameters}, return_type={self.return_type})"


class FunctionMetadata:
    def __init__(self, name, parameters, body, return_type=None):
        self.name = name
        self.overloads = []
        self.overloads.append(FunctionOverload(parameters, return_type, body)) # Add the first overload

    def add_overload(self, parameters, return_type, body):
        """
        Add a new overload to the function
        We only check for the number of parameters since we don't know the sl_types of the parameters
        :param parameters:
        :param return_type:
        :param body:
        :return:
        """
        # Check for existing overload with the same parameter count
        for overload in self.overloads:
            if overload.matches(parameters):
                raise VariableRedeclaredError(
                    f"Function '{self.name}' with {len(parameters)} parameters already declared."
                )

        # Add the new overload
        new_overload = FunctionOverload(parameters, return_type, body)
        self.overloads.append(new_overload)

    def has_overload(self, parameter_count):
        return any(len(overload.parameters) == parameter_count for overload in self.overloads)


    def find_overload(self, parameters):
        for overload in self.overloads:
            if overload.matches(parameters):
                return overload
        raise FunctionNotFoundError(
            f"No matching overload found for function '{self.name}' with {len(parameters)} arguments."
        )

    def merge(self, other):
        """
        Merge another FunctionMetadata into this one, ensuring no incompatible overloads exist.

        :param other: Another FunctionMetadata instance.
        :raises VariableRedeclaredError: If merging causes overload conflicts.
        """
        if self.name != other.name:
            raise ValueError("Cannot merge FunctionMetadata with different names.")

        for overload in other.overloads:
            # Check for conflicts before adding
            if any(existing_overload.matches(overload.parameters) for existing_overload in self.overloads):
                raise VariableRedeclaredError(
                    f"Cannot merge overload with {len(overload.parameters)} parameters into function '{self.name}'; overload already exists."
                )
            # If no conflict, add the overload
            self.overloads.append(overload)

    def __repr__(self):
        return f"FunctionMetadata(name={self.name}, overloads={self.overloads})"

    def remove_overload(self, parameter_count):
        for overload in self.overloads:
            if len(overload.parameters) == parameter_count:
                self.overloads.remove(overload)
                return True
            return False

    def list_overloads(self):
        return [f"Parameters: {overload.parameters}, Return Type: {overload.return_type}"
                for overload in self.overloads]


    def dump(self):
        for entry in self.list_overloads():
            print(entry)

    def cleanup(self):
        self.name = None
        self.overloads.clear()
        self.overloads = None


    def __add__ (self, other):
        if isinstance(other, FunctionMetadata):
            if self.name == other.name:
                initial_overloads = self.overloads

        return NotImplemented