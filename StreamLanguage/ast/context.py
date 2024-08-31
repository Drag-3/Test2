import uuid

from symbol_table import SymbolTable
from exceptions import VariableNotDeclaredError, FunctionNotFoundError, SLRecursionError


class Context:
    MAX_RECURSION_DEPTH = 1000  # Set a limit to prevent stack overflow or infinite recursion



    def __init__(self, parent=None):
        self.parent = parent
        self.global_symbol_table = SymbolTable() if parent is None else parent.global_symbol_table
        self.local_symbol_tables = [SymbolTable()]  # Stack of local symbol tables
        self.function_calls = []
        self.blocks_stack = []  # Stack to manage block UUIDs
        self.recursion_depth = {}
        self.current_block_uuid = None
        self.call_stack = []  # Stack to maintain function call trace
        self.loop_stack = []  # Stack to manage loop states


    def _get_global_symbol_table(self):
        if self.parent:
            return self.parent._get_global_symbol_table()
        return self.global_symbol_table

    # Variable and Type Management
    def get_type(self, identifier):
        context = self
        while context is not None:
            for symbol_table in reversed(context.local_symbol_tables):
                if symbol_table.is_declared(identifier):
                    return symbol_table.lookup(identifier).type
            context = context.parent

        if identifier in self.global_symbol_table:
            return self.global_symbol_table[identifier]

        raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared in the current scope.")

    def set_type(self, identifier, t, global_scope=False):
        # Set type in the appropriate scope (global or local)
        if global_scope:
            self.global_symbol_table[identifier] = t
        else:
            self.local_symbol_tables[-1].lookup(identifier).type = t

    def declare_variable(self, identifier, t=None, value=None):


        # Ensure variable is not declared in any parent context to prevent shadowing in the same block
        if self.parent:
            if self.parent.is_declared(identifier):
                raise Exception(f"Variable '{identifier}' already declared in an outer scope")

        # Declare the variable in the current local scope
        self.local_symbol_tables[-1].declare(identifier, t, value)

    def is_declared(self, identifier):
        for symbol_table in reversed(self.local_symbol_tables):
            if symbol_table.is_declared(identifier):
                return True
        if self.global_symbol_table.is_declared(identifier):
            return True
        return False

    def assign(self, identifier, value):
        for symbol_table in reversed(self.local_symbol_tables):
            if symbol_table.is_declared(identifier):
                symbol_table.update(identifier, value)
                return
        if self.global_symbol_table.is_declared(identifier):
            self.global_symbol_table.update(identifier, value)
        else:
            raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared in the current scope.")

    def lookup(self, identifier):
        for symbol_table in reversed(self.local_symbol_tables):
            if symbol_table.is_declared(identifier):
                return symbol_table.lookup(identifier).value
        if self.global_symbol_table.is_declared(identifier):
            return self.global_symbol_table.lookup(identifier).value
        if self.parent:
            return self.parent.lookup(identifier)
        raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared in the current scope.")


    # Block Management
    def enter_block(self, block_uuid):
        self.blocks_stack.append(self.current_block_uuid)
        self.current_block_uuid = block_uuid
        self.local_symbol_tables.append(SymbolTable())  # New scope for the block

    def exit_block(self):
        if self.local_symbol_tables:
            self.local_symbol_tables.pop()
        if self.blocks_stack:
            self.current_block_uuid = self.blocks_stack.pop()
        else:
            self.current_block_uuid = None

    def get_current_block_uuid(self):
        return self.current_block_uuid

    def _clean_up_variables(self):
        # Clean up variables declared in the current block
        if self.local_symbol_tables:
            self.local_symbol_tables.pop()

    # Scope Management
    def enter_scope(self):
        self.local_symbol_tables.append(SymbolTable())

    def exit_scope(self):
        self.local_symbol_tables.pop()

    # Function Call Management
    def enter_function_call(self, function_name):
        if function_name in self.recursion_depth:
            self.recursion_depth[function_name] += 1
            if self.recursion_depth[function_name] > self.MAX_RECURSION_DEPTH:
                raise SLRecursionError(f"Exceeded maximum recursion depth in function '{function_name}'")
        else:
            self.recursion_depth[function_name] = 1

        new_context = Context(parent=self)
        new_context.enter_scope()
        new_context.function_calls.append(function_name)
        new_context.call_stack.append(function_name)
        self.enter_block(str(uuid.uuid4()))  # Assign a new block UUID for the function scope
        return new_context


    def exit_function_call(self, function_name):
        if function_name in self.call_stack:
            self.call_stack.pop()
        if function_name in self.recursion_depth:
            self.recursion_depth[function_name] -= 1
            if self.recursion_depth[function_name] == 0:
                del self.recursion_depth[function_name]
        self.exit_scope()
        self.exit_block()

    def declare_function(self, name, function_callable, global_scope=False):
        """
        Declare a function in the appropriate symbol table.
        :param name: The name of the function.
        :param function_callable: The callable function object.
        :param global_scope: A flag indicating whether the function should be declared in the global scope
        """
        if global_scope:
            self.global_symbol_table.declare(name, t='function', value=function_callable)
        else:
            self.local_symbol_tables[-1].declare(name, t='function', value=function_callable)


    def store_function(self, name, function, function_context):
        """Stores a function and its context in the global symbol table."""
        self.global_symbol_table.declare(name, t='function', value={'function': function, 'context': function_context})

    def lookup_function(self, name):
        for symbol_table in reversed(self.local_symbol_tables):
            if symbol_table.is_declared(name):
                entry = symbol_table.lookup(name)
                if entry.type == 'function':
                    return entry.value
        if self.global_symbol_table.is_declared(name):
            entry = self.global_symbol_table.lookup(name)
            if entry.type == 'function':
                return entry.value
        raise FunctionNotFoundError(f"Function '{name}' is not defined in the current scope.")


    def handle_return(self, value):
        self.return_value = value


    # Loop Management
    def enter_loop(self, loop_uuid):
        self.loop_stack.append(loop_uuid)

    def exit_loop(self):
        self.loop_stack.pop()

    def get_current_loop(self):
        return self.loop_stack[-1] if self.loop_stack else None

    # Debugging and Tracing
    def dump_state(self):
        print("Current Block UUID:", self.current_block_uuid)
        print("Current Symbol Table:", self.local_symbol_tables[-1])
        print("Global Symbol Table:", self.global_symbol_table)
        print("Function Calls:", self.function_calls)
        print("Call Stack:", self.call_stack)
        print("Block Stack:", self.blocks_stack)
        print("Loop Stack:", self.loop_stack)
        print("Recursion Depth:", self.recursion_depth)

    # Cloning Context
    def clone(self):
        new_context = Context(parent=self.parent)
        new_context.global_symbol_table = self.global_symbol_table.copy()
        new_context.local_symbol_tables = [table.copy() for table in self.local_symbol_tables]
        new_context.function_calls = self.function_calls.copy()
        new_context.blocks_stack = self.blocks_stack.copy()
        new_context.recursion_depth = self.recursion_depth.copy()
        new_context.current_block_uuid = self.current_block_uuid
        new_context.call_stack = self.call_stack.copy()
        new_context.loop_stack = self.loop_stack.copy()
        return new_context

    def reset(self):
        self.local_symbol_tables = [{}]
        self.function_calls = []
        self.blocks_stack = []
        self.recursion_depth = {}
        self.current_block_uuid = None
        self.call_stack = []
        self.loop_stack = []