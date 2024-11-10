from contextlib import contextmanager

from StreamLanguage.interpreter.function_metadata import FunctionMetadata
from StreamLanguage.interpreter.symbol_table import SymbolTable

from StreamLanguage.ast.exceptions import SLRecursionError
from StreamLanguage.interpreter.block import Block
from StreamLanguage.interpreter.callframe import CallFrame


class Context:
    def __init__(self, parent=None, context_type=None):
        self.MAX_RECURSION_DEPTH = 1000
        self.parent = parent
        self.context_type = context_type or 'generic'
        self.current_symbol_table = SymbolTable(parent=self.parent.current_symbol_table if self.parent else None)
        # Other attributes remain the same
        self.blocks_stack = []  # Stack to manage block UUIDs
        self.recursion_depth = {}
        self.call_stack = []  # Stack to maintain function call trace
        self.loop_stack = []  # Stack to manage loop states

    def enter_scope(self):
        self.current_symbol_table = SymbolTable(parent=self.current_symbol_table)

    def exit_scope(self):
        if self.current_symbol_table.parent:
            self.current_symbol_table = self.current_symbol_table.parent
        else:
            raise Exception("Cannot exit the global scope")

    def enter_block(self, block_type):
        block = Block(block_type)
        self.blocks_stack.append(block)
        self.current_symbol_table = SymbolTable(parent=self.current_symbol_table)

    def exit_block(self):
        if self.blocks_stack:
            self.blocks_stack.pop()
            self.current_symbol_table = self.current_symbol_table.parent

    def can_define_function(self):
        if self.blocks_stack:
            return self.blocks_stack[-1].can_define_function()
        return True  # Default to allowing functions at the global scope

    def declare_variable(self, identifier, t=None, value=None):
        self.current_symbol_table.declare(identifier, t, value)

    def declare_function(self, identifier, callable_object, parameters, return_type=None):
        # Check if functions can be defined in the current context
        if not self.can_define_function():
            raise Exception("Cannot define functions in the current context")

        # Create a function Metadata object
        metadata = FunctionMetadata(identifier, callable_object, parameters, return_type)

        # Declare the function in the symbol table // overloads handled in SymbolTable
        self.current_symbol_table.declare_function(metadata)


    def lookup(self, identifier):
        return self.current_symbol_table.lookup(identifier).value

    def assign(self, identifier, value):
        self.current_symbol_table.update(identifier, value)

    @contextmanager
    def function_call_context(self, function_node, arguments):
        self.enter_function_call(function_node, arguments)
        try:
            yield
        finally:
            self.exit_function_call()

    def enter_function_call(self, function_node, arguments):
        # Check recursion limits
        if function_node.name in self.recursion_depth:
            self.recursion_depth[function_node.name] += 1
            if self.recursion_depth[function_node.name] > self.MAX_RECURSION_DEPTH:
                raise SLRecursionError(f"Exceeded maximum recursion depth in function '{function_node.name}'")
        else:
            self.recursion_depth[function_node.name] = 1
        # Create a new symbol table for the function scope
        function_symbol_table = SymbolTable(parent=self.current_symbol_table, is_restricted=True)
        self.current_symbol_table = function_symbol_table

        # Assign arguments to the function parameters
        for param, arg in zip(function_node.parameters, arguments):
            self.current_symbol_table.declare(param.name, value=arg)

        # Push a detailed call frame onto the call stack
        call_frame = CallFrame(function_node.name, arguments, self.current_symbol_table)
        self.call_stack.append(call_frame)

    def exit_function_call(self):
        # Pop the call frame and restore the previous symbol table
        if self.call_stack:
            call_frame = self.call_stack.pop()
            self.current_symbol_table = self.current_symbol_table.parent

            # Decrement recursion depth for this function
            function_name = call_frame.function_name
            if self.recursion_depth[function_name] > 0:
                self.recursion_depth[function_name] -= 1
            if self.recursion_depth[function_name] == 0:
                del self.recursion_depth[function_name]  # Cleanup recursion tracking

    def execute_function(self, function_node, arguments):
        try:
            with self.function_call_context(function_node, arguments):
                # Function execution logic
                pass
        except Exception as e:

            raise e

    def get_call_stack_trace(self):
        trace = ""
        for frame in reversed(self.call_stack):
            trace += f"Function '{frame.function_name}' called with arguments {frame.arguments}\n"
        return trace