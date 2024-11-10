from StreamLanguage.ast.exceptions import VariableNotDeclaredError, SLTypeError, VariableRedeclaredError


class SymbolTableEntry:
    def __init__(self, identifier, t=None, value=None, is_constant=False, scope_level=None, is_global=False, is_nonlocal=False):
        self.identifier = identifier  # The name of the variable or symbol
        self.type = t  # The type of the symbol (optional)
        self.value = value  # The value associated with the symbol (optional)
        self.scope_level = scope_level  # The scope level at which the symbol was declared
        self.is_constant = is_constant

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
"""
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
        """"""
        Declare a function in the symbol table.

        :param metadata: FunctionMetadata
        :return:
        """"""
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
"""


class SymbolTable:
    def __init__(self, parent=None, is_restricted=False):
        self.parent = parent
        self.is_restricted = is_restricted
        self.entries = {}
        self.nonlocal_entries = set() # Set of nonlocal variables only store the name of the variable

    def declare(self, identifier, t, value=None, is_constant=False, is_global=False, is_nonlocal=False):
        # Check for shadowing
        if identifier in self.entries:
            raise VariableRedeclaredError(f"Variable '{identifier}' already declared")
        if is_nonlocal:
            self.nonlocal_entries.add(identifier)
        else:
            self.entries[identifier] = SymbolTableEntry(identifier, t, value, is_constant, is_global=is_global)


    def is_declared(self, identifier):
        if identifier in self.entries:
            return True
        elif self.parent:
            return self.parent.is_declared(identifier)
        else:
            return False

    
    def lookup(self, identifier):
        if identifier in self.entries:  # Declared in the current scope
            return self.entries[identifier]

        if identifier in self.nonlocal_entries:  # Explicitly declared as nonlocal, this works in any scope type
            return self._parent_lookup(identifier)

        if self.is_restricted: # Restricted scope, no access to parent scopes (functions)
            raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared.")

        return self._parent_lookup(identifier)  # Non strict mode, look in parent scopes

    def _parent_lookup(self, identifier):
        current_scope = self.parent
        while current_scope:
            entry = current_scope.entries.get(identifier)
            if entry:
                return entry
            current_scope = current_scope.parent
        raise VariableNotDeclaredError(f"Nonlocal variable '{identifier}' is not declared in any accessible scope.")

    def update(self, identifier, value):
        if identifier in self.entries:
            entry = self.entries[identifier]
            if entry.is_constant:
                raise Exception("Cannot reassign value to a constant variable")
            entry.value = value
        elif self.parent:
            if self.is_restricted and identifier not in self.nonlocal_entries:  # Restricted scope, no access to parent scopes unless nonlocal
                raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared.")
            self.parent.update(identifier, value)
        else:
            raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared.")

    def declare_function(self, metadata):
        if not self.is_declared(metadata.name):
            self.declare(metadata.name, 'function', metadata)
        else:
            # Try to add the overload
            entry = self.lookup(metadata.name)
            if entry.type != 'function':
                raise SLTypeError(f"Symbol '{metadata.name}' is not a function")
            # Apply the new overload
            entry.value.merge(metadata)

    def cleanup(self):
        for entry in self.entries.values():
            entry.cleanup()
        self.entries.clear()