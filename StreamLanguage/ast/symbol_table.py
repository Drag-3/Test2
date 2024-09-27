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

    def declare_function(self, identifier, value):
        """
        Declare a function in the symbol table.
        :param identifier: The name of the function
        :param type: The optional return type of the function
        :param value: A Data Struction Containing the function callable, type, and parameters
        :return:
        """
        if identifier in self.entries:
            # Get the amount of parameters in the existing function
            num_params = len(self.entries[identifier].get('parameters', []))

            if num_params == len(value.get('parameters', [])):
                # Due to dynamic typing, we can't guarantee that the function signatures are the same,
                # So ill err on the side of caution and not allow redeclaration
                raise VariableRedeclaredError(f"Function '{identifier}' already declared")
            else:
                # Add the function as an overload
                self.entries[identifier].add_overload(SymbolTableEntry(identifier, 'function', value))

        else:
            self.entries[identifier] = SymbolTableEntry(identifier, 'function', value)

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
