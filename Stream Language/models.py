

class Type:
    def __init__(self, name: str):
        self.name = name

class StringType(Type):
    def __init__(self):
        super().__init__("string")

class IntType(Type):
    def __init__(self):
        super().__init__("int")

class BoolType(Type):
    def __init__(self):
        super().__init__("bool")

class UndefinedType(Type):
    def __init__(self):
        super().__init__("undefined")
class Variable:
    def __init__(self, name:str, value=None, type=None):
        self.name = name

        # Initial Assignment
        if type is None:
            if value is None:
                self.type = UndefinedType()
            else:
                self.type = type_fromPython(value)
                self.value = value
        else:
            if value is None:
                self.type = type
                self.value = None
            else:
                if type(value) == type:
                    self.type = type
                    self.value = value
                else:
                    raise ValueError("Type mismatch")

    def assign(self, value):
        if self.type == UndefinedType:
            self.type = type(value)
        elif self.type != type(value):
            raise ValueError("Type mismatch")
        self.value = value
