class FunctionOverload:
    def __init__(self, parameters, return_type, body):
        self.parameters = parameters
        self.return_type = return_type
        self.implementation = body

    def __repr__(self):
        return f"FunctionOverload(parameters={self.parameters}, return_type={self.return_type})"


class FunctionMetadata:
    def __init__(self, name, parameters, body, return_type=None):
        self.name = name
        self.overloads = []
        self.overloads.append(FunctionOverload(parameters, return_type, body))

    def add_overload(self, parameters, return_type, body):
        if self.find_overload(parameters) is not None:
            raise Exception("Function overload already exists")
        self.overloads.append(FunctionOverload(parameters, return_type, body))

    def has_overload(self, parameter_count):
        return any(len(overload.parameters) == parameter_count for overload in self.overloads)


    def find_overload(self, parameters):
        for overload in self.overloads:
            if len(overload.parameters) == len(parameters):
                return overload
        return None

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