import uuid

from StreamLanguage.ast.function_metadata import FunctionMetadata
from StreamLanguage.ast.symbol_table import SymbolTable
from StreamLanguage.ast.exceptions import VariableNotDeclaredError, FunctionNotFoundError, SLRecursionError, \
    FunctionDeclarationError, VariableRedeclaredError
from StreamLanguage.ast.block_types import BlockFlags, BlockType


class Context:
    MAX_RECURSION_DEPTH = 1000  # Set a limit to prevent stack overflow or infinite recursion



    def __init__(self, parent=None, context_type=None):
        self.parent = parent
        self.context_type = context_type or 'generic'  # Default to 'generic' if not specified
        self.global_symbol_table = SymbolTable() if parent is None else parent.global_symbol_table
        self.local_symbol_tables = [SymbolTable()]  # Stack of local symbol tables
        self.blocks_stack = []  # Stack to manage block UUIDs
        self.recursion_depth = {}
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
            return self.global_symbol_table[identifier].type

        raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared in the current scope.")

    def set_type(self, identifier, t, global_scope=False):
        # Set type in the appropriate scope (global or local)
        if global_scope:
            self.global_symbol_table[identifier] = t
        else:
            self.local_symbol_tables[-1].lookup(identifier).type = t

    def declare_variable(self, identifier, t=None, value=None):
        current_symbol_table = self.local_symbol_tables[-1]

        # Prevent redeclaration in the same scope
        if current_symbol_table.is_declared(identifier):
            raise VariableRedeclaredError(f"Variable '{identifier}' already declared in the current scope")

        current_symbol_table.declare(identifier, t, value)

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
        # Check local scopes from nearest to farthest
        for symbol_table in reversed(self.local_symbol_tables):
            if symbol_table.is_declared(identifier):
                return symbol_table.lookup(identifier).value

        # Fallback to global scope
        if self.global_symbol_table.is_declared(identifier):
            return self.global_symbol_table.lookup(identifier).value

        # If not found anywhere, handle the error
        raise VariableNotDeclaredError(f"Variable '{identifier}' is not declared in the current scope.")

    # Block Management
    def get_current_block_uuid(self):
        if self.blocks_stack:
            return self.blocks_stack[-1][0]  # Return the UUID of the topmost block
        return None  # Return None if there are no blocks

    def get_current_block_type(self):
        if self.blocks_stack:
            block_type_flags = self.blocks_stack[-1][1]
            for block_type in BlockType:
                if block_type.value == block_type_flags:
                    return block_type
        return BlockType.PROGRAM

    def get_current_block_flags(self):
        return self.get_current_block_type().value

    def enter_block(self, block_uuid, block_type=BlockType.DEFAULT):
        # Push the new block information onto the stack
        self.blocks_stack.append((block_uuid, block_type))
        self.enter_scope()  # Create a new symbol table scope for this block

    def can_define_function(self):
        current_block_type = self.get_current_block_type()
        return (current_block_type.value & BlockFlags.ALLOW_FUNCTIONS) != 0

    def exit_block(self):
        # First, handle any variable cleanups
        self._clean_up_variables()
        # Then, exit the scope associated with this block
        self.exit_scope()
        # Finally, remove the block from the stack
        if self.blocks_stack:
            self.blocks_stack.pop()

    def _clean_up_variables(self):
        # Clean up variables declared in the current block
        if self.local_symbol_tables:
            current_symbol_table = self.local_symbol_tables[-1]
            current_symbol_table.cleanup()

    # Scope Management
    def enter_scope(self):
        self.local_symbol_tables.append(SymbolTable())

    def exit_scope(self):
        if self.local_symbol_tables:
            self.local_symbol_tables.pop()

    # Function Call Management
    def enter_function_call(self, function_node, arguments):
        # Check recursion limits
        if function_node.name in self.recursion_depth:
            self.recursion_depth[function_node.name] += 1
            if self.recursion_depth[function_node.name] > self.MAX_RECURSION_DEPTH:
                raise SLRecursionError(f"Exceeded maximum recursion depth in function '{function_node.name}'")
        else:
            self.recursion_depth[function_node.name] = 1

        block_uuid = str(uuid.uuid4())
        self.enter_block(block_uuid, BlockType.FUNCTION)  # Track the function call block

        # Create a new context for the function call
        new_context = Context(parent=self, context_type='function')
        new_context.call_stack.append(function_node.name)  # Add the function name to the call stack

        # Assign arguments to the function parameters
        for param, arg in zip(function_node.parameters, arguments):
            new_context.declare_variable(param.name, value=arg)


        return new_context

    def exit_function_call(self, child_context):
        if not child_context:  # No child context to exit
            return

        # Cleanup any block-level resources
        child_context.exit_block()

        # Pop the function call and context from the parent's call stack
        if self.call_stack:
            self.call_stack.pop()

        # Decrement recursion depth for this function
        function_name = child_context.call_stack[-1]  # Get the function name from child context
        if self.recursion_depth[function_name] > 0:
            self.recursion_depth[function_name] -= 1
        if self.recursion_depth[function_name] == 0:
            del self.recursion_depth[function_name]  # Cleanup recursion tracking

        # Additional cleanup if necessary
        child_context.cleanup()

    def declare_function(self, name, function_callable, parameters, return_type, global_scope=False):
        if not self.can_define_function():
            raise FunctionDeclarationError(f"Cannot declare function '{name}' in this block type.")

        # Create a new function metadata object
        function_metadata = FunctionMetadata(name, parameters, function_callable, return_type)

        # Add function to correct scope
        if global_scope:
            self.global_symbol_table.declare_function(function_metadata)
        else:
            self.local_symbol_tables[-1].declare_function(function_metadata)

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

    def handle_return(self, return_value):
        # Process the return value here, maybe modify it or log it
        print(f"Function returned: {return_value}")  #Logging for debugging

        return return_value

    def is_recursive_call(self, caller, callee):
        return callee in self.call_stack
    # Loop Management
    def enter_loop(self):  # IDK if I need these functions, was just adding stuff
        loop_uuid = str(uuid.uuid4())
        self.loop_stack.append(loop_uuid)
        self.enter_block(loop_uuid, BlockType.LOOP)  # Enter a new block for the loop

    def exit_loop(self):
        self.exit_block()  # Exit the loop block
        if self.loop_stack:
            self.loop_stack.pop()

    def get_current_loop(self):
        return self.loop_stack[-1] if self.loop_stack else None

    def enter_if_block(self):
        block_uuid = str(uuid.uuid4())
        self.enter_block(block_uuid, BlockType.IF)

    def exit_if_block(self):
        self.exit_block()

    def enter_else_block(self):
        block_uuid = str(uuid.uuid4())
        self.enter_block(block_uuid, BlockType.ELSE)

    def exit_else_block(self):
        self.exit_block()

    def enter_try(self):
        block_uuid = str(uuid.uuid4())
        self.enter_block(block_uuid, BlockType.TRY)

    def exit_try(self):
        self.exit_block()

    def enter_catch(self, exception):
        block_uuid = str(uuid.uuid4())
        self.enter_block(block_uuid, BlockType.CATCH)

    def exit_catch(self):
        self.exit_block()

    def enter_finally(self):
        block_uuid = str(uuid.uuid4())
        self.enter_block(block_uuid, BlockType.FINALLY)

    def exit_finally(self):
        self.exit_block()

    # Debugging and Tracing
    def dump_state(self):  # This is just for debugging But I should set it up to call this during a fatal error to get a better stacktrace
        print("Current Block UUID:", self.get_current_block_uuid())
        print("Current Symbol Table:", self.local_symbol_tables[-1])
        print("Global Symbol Table:", self.global_symbol_table)
        print("Call Stack:", self.call_stack)
        print("Block Stack:", self.blocks_stack)
        print("Loop Stack:", self.loop_stack)
        print("Recursion Depth:", self.recursion_depth)

    # Cloning Context
    def clone(self):
        new_context = Context(parent=self.parent)
        new_context.global_symbol_table = self.global_symbol_table.copy()
        new_context.local_symbol_tables = [table.copy() for table in self.local_symbol_tables]
        new_context.blocks_stack = self.blocks_stack.copy()
        new_context.recursion_depth = self.recursion_depth.copy()
        new_context.call_stack = self.call_stack.copy()
        new_context.loop_stack = self.loop_stack.copy()
        return new_context

    def cleanup(self):
        # Cleanup all local symbol tables
        for symbol_table in self.local_symbol_tables:
            symbol_table.cleanup()
        self.local_symbol_tables.clear()

        # Cleanup global symbol table only if it's not shared
        if self.parent is None:
            self.global_symbol_table.cleanup()

        # Clear all other attributes This may or may not result in a usable context
        self.blocks_stack.clear()
        self.recursion_depth.clear()
        self.call_stack.clear()
        self.loop_stack.clear()

    def reset(self):
        # Reset local symbol tables
        self.local_symbol_tables = [SymbolTable()]

        # Optionally reset the global symbol table if it's not shared
        if self.parent is None:
            self.global_symbol_table.reset()

        # Reset all lists and dictionaries, but keep the structure
        self.blocks_stack = []
        self.recursion_depth = {}
        self.call_stack = []
        self.loop_stack = []