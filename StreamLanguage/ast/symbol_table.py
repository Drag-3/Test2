from StreamLanguage.ast.exceptions import VariableNotDeclaredError, SLTypeError, VariableRedeclaredError


class SymbolTableEntry:
    def __init__(self, identifier, t=None, value=None, is_constant=False, scope_level=None):
        self.identifier = identifier  # The name of the variable or symbol
        self.type = t  # The type of the symbol (optional)
        self.value = value  # The value associated with the symbol (optional)
        self.scope_level = scope_level  # The scope level at which the symbol was declared
        self.is_constant = is_constant
        self.overloads = []  # List to store overloads or additional entries if necessary

    def add_overload(self, entry):
        self.overloads.append(entry)

    def __repr__(self):
        return f"SymbolTableEntry(identifier={self.identifier}, type={self.type}, value={self.value}, scope_level={self.scope_level}, is_constant={self.is_constant})"

    def cleanup(self):
        # If 'value' is a resource that needs to be explicitly closed
        if hasattr(self.value, 'close'):
            try:
                self.value.close()
            except Exception as e:
                print(f"Failed to close resource for {self.identifier}: {str(e)}")

        # Clear the references to help with garbage collection
        self.identifier = None
        self.type = None
        self.value = None
        self.scope_level = None
        self.is_constant = None

class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.entries = {}

    def declare(self, identifier, t, value=None, is_constant=False):
        if identifier in self.entries:
            raise VariableRedeclaredError(f"Variable '{identifier}' already declared")
        self.entries[identifier] = SymbolTableEntry(identifier, t, value, is_constant)

    def update(self, identifier, value):
        if identifier not in self.entries:
            raise VariableNotDeclaredError(f"Variable '{identifier}' not declared")
        entry = self.entries[identifier]
        if entry.is_constant:
            raise Exception("Cannot reassign value to a constant variable")
        entry.value = value

    def lookup(self, identifier):
        return self.entries.get(identifier, None)

    def declare_function(self, metadata):
        """
        Declare a function in the symbol table.

        :param metadata: FunctionMetadata
        :return:
        """
        if not self.is_declared(metadata.name):
            self.declare(metadata.name,'function', metadata)
        else:
            # Try to add the overload
            entry = self.lookup(metadata.name)
            if entry.type != 'function':
                raise SLTypeError(f"Symbol '{metadata.name}' is not a function")
            entry.value.merge(metadata)


    def is_declared(self, identifier):
        return identifier in self.entries

    def cleanup(self):
        for entry in self.entries.values():
            entry.cleanup()
        self.entries.clear()

    def __repr__(self):
        return f"SymbolTable({self.entries})"

    def __getitem__(self, item):
        return self.entries[item]

    def __setitem__(self, key, value):
        self.entries[key] = value
