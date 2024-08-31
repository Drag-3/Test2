from .exceptions import VariableNotDeclaredError, TypeError

class SymbolTableEntry:
    def __init__(self, identifier, t=None, value=None):
        self.identifier = identifier  # The name of the variable or symbol
        self.type = t  # The type of the symbol (optional)
        self.value = value  # The value associated with the symbol (optional)
        self.scope_level = None
        self.is_constant = False

    def __repr__(self):
        return f"SymbolTableEntry(identifier={self.identifier}, type={self.type}, value={self.value}, scope_level={self.scope_level}, is_constant={self.is_constant})"

class SymbolTable:
    def __init__(self):
        self.table = {}  # Dictionary to store symbols

    def declare(self, identifier, t=None, value=None, is_constant=False):
        if identifier in self.table:
            raise VariableNotDeclaredError(f"Variable '{identifier}' already declared in this scope")
        entry = SymbolTableEntry(identifier, t, value)
        entry.is_constant = is_constant
        self.table[identifier] = entry

    def update(self, identifier, value):
        if identifier not in self.table:
            raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared")

        entry = self.table[identifier]

        if entry.is_constant:
            raise Exception(f"Cannot reassign value to constant '{identifier}'")

        # Determine the type of the new value
        new_type = type(value)

        if entry.type is None:
            # If the type hasn't been set, set it now
            entry.type = new_type
        elif entry.type != new_type:
            raise TypeError(
                f"Type mismatch for variable '{identifier}': expected {entry.type.__name__}, but got {new_type.__name__}")

        # Update the value
        entry.value = value

    def lookup(self, identifier):
        if identifier not in self.table:
            raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared")
        return self.table[identifier]

    def is_declared(self, identifier):
        return identifier in self.table

    def copy(self):
        new_table = SymbolTable()
        new_table.table = self.table.copy()
        return new_table

    def __getitem__(self, identifier):
        return self.lookup(identifier).value

    def __setitem__(self, identifier, value):
        self.update(identifier, value)

    def __contains__(self, identifier):
        return identifier in self.table

    def __repr__(self):
        return f"SymbolTable({self.table})"