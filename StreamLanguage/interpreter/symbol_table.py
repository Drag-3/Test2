from StreamLanguage.sl_ast.exceptions import VariableNotDeclaredError, SLTypeError, VariableRedeclaredError
from StreamLanguage.interpreter.function_metadata import FunctionMetadata
from StreamLanguage.sl_types.base import SLType


class SymbolTableEntry:
    def __init__(self, identifier, t=None, value=None, is_constant=False, scope_level=None, is_global=False, is_nonlocal=False):
        self.identifier = identifier  # The name of the variable or symbol
        self.type = t  # The type of the symbol (optional)
        self.value = value  # The value associated with the symbol (optional)  // Never set if nonlocal
        self.scope_level = scope_level  # The scope level at which the symbol was declared
        self.is_constant = is_constant
        self.non_local = is_nonlocal
        self.global_scope = is_global

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
    def __init__(self, parent=None, is_restricted=False, global_symbol_table=None):
        self.parent = parent
        self.is_restricted = is_restricted
        self.global_symbol_table = global_symbol_table or (parent.global_symbol_table if parent else self)  # Global symbol table
        self.entries = {}
        self.nonlocal_entries = set()

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
        if identifier in self.entries:
            return self.entries[identifier]
        elif self.is_restricted:
            if identifier in self.nonlocal_entries:  # Check nonlocal entries
                return self._parent_lookup(identifier)
            else:  # Restricted scope, no access to parent scopes except global
                return self.global_symbol_table.lookup(identifier)
        elif self.parent:
            return self.parent.lookup(identifier)
        else:
            raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared.")

    def lookup_type(self, identifier):
        entry = self.lookup(identifier)
        if not entry.type:
            return None  # No type specified or Null
        return entry.type()

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
        elif self.is_restricted:
            if identifier in self.nonlocal_entries:
                self._parent_update(identifier, value)
            else:
                self.global_symbol_table.update(identifier, value)
        elif self.parent:
            self.parent.update(identifier, value)
        else:
            raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared.")

    def _parent_update(self, identifier, value):
        current_scope = self.parent
        while current_scope:
            entry = current_scope.entries.get(identifier)
            if entry:
                if entry.is_constant:
                    raise Exception("Cannot reassign value to a constant variable")
                entry.value = value
                return
            current_scope = current_scope.parent
        raise VariableNotDeclaredError(f"Nonlocal variable '{identifier}' is not declared in any accessible scope.")

    def update_type(self, identifier, t: SLType):
        if identifier in self.entries:
            entry = self.entries[identifier]
            entry.type = t
        elif self.parent:
            if self.is_restricted and identifier not in self.nonlocal_entries:
                raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared.")
            self.parent.update_type(identifier, t)
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

    def lookup_function(self, identifier, params):
        entry = self.lookup(identifier)
        if entry.type != 'function':
            raise SLTypeError(f"Symbol '{identifier}' is not a function")
        f_overload: FunctionMetadata = entry.value.find_overload(params)
        if not f_overload:
            raise SLTypeError(f"Function '{identifier}' does not accept the given parameters")
        return f_overload


    def cleanup(self):
        for entry in self.entries.values():
            entry.cleanup()
        self.entries.clear()