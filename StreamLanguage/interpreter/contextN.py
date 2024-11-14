from contextlib import contextmanager

from StreamLanguage.ast.callables import CallableFunction
from StreamLanguage.ast.exceptions import SLRecursionError, FunctionNotFoundError
from StreamLanguage.ast.nodes.base import ParserNode
from StreamLanguage.exceptions import SLException
from StreamLanguage.interpreter.block import Block
from StreamLanguage.interpreter.callframe import CallFrame
from StreamLanguage.interpreter.flow_manager import ControlFlowManager
from StreamLanguage.interpreter.function_metadata import FunctionMetadata
from StreamLanguage.interpreter.symbol_table import SymbolTable
from StreamLanguage.sl_types.data_instances.instance_base import SLInstanceType


class Context:
    def __init__(self, parent=None, context_type=None):
        self.MAX_RECURSION_DEPTH = 1000
        self.parent = parent
        self.context_type = context_type or 'generic'
        self.current_symbol_table = SymbolTable(parent=self.parent.current_symbol_table if self.parent else None)
        # Other attributes remain the same
        self.blocks_stack = []  # Stack to manage block UUIDs
        self.recursion_depth = {}
        self.control_flow = ControlFlowManager()
        self.call_stack = []  # Stack to maintain function call trace
        self.loop_stack = []  # Stack to manage loop states

    def enter_scope(self):
        self.current_symbol_table = SymbolTable(parent=self.current_symbol_table)

    def exit_scope(self):
        if self.current_symbol_table.parent:
            self.current_symbol_table = self.current_symbol_table.parent
        else:
            raise Exception("Cannot exit the global scope")

    def enter_block(self, block_type, block_uuid):
        block = Block(block_type, block_uuid)
        self.blocks_stack.append(block)
        self.current_symbol_table = SymbolTable(parent=self.current_symbol_table)

    def exit_block(self):
        if self.blocks_stack:
            self.blocks_stack.pop()
            self.current_symbol_table = self.current_symbol_table.parent

    @contextmanager
    def block_context(self, block_type, block_uuid):
        self.enter_block(block_type, block_uuid)
        try:
            yield
        finally:
            self.exit_block()


    @contextmanager
    def scope_context(self):
        self.enter_scope()
        try:
            yield
        finally:
            self.exit_scope()

    def can_define_function(self):
        if self.blocks_stack:
            return self.blocks_stack[-1].can_define_function()
        return True  # Default to allowing functions at the global scope

    def declare_variable(self, identifier, t=None, v=None):
        self.current_symbol_table.declare(identifier, t, v)

    def declare_function(self, identifier, callable_object, parameters, return_type=None):
        # Check if functions can be defined in the current context
        if not self.can_define_function():
            raise Exception("Cannot define functions in the current context")

        # Create a function Metadata object
        metadata = FunctionMetadata(identifier, parameters, callable_object, return_type)

        # Declare the function in the symbol table // overloads handled in SymbolTable
        self.current_symbol_table.declare_function(metadata)


    def lookup(self, identifier):
        return self.current_symbol_table.lookup(identifier).value

    def lookup_function(self, identifier, parameters):
        return self.current_symbol_table.lookup_function(identifier, parameters)

    def assign(self, identifier, value):
        self.current_symbol_table.update(identifier, value)

    @contextmanager
    def function_call_context(self, function_node, arguments):
        self.enter_function_call(function_node, arguments)
        try:
            yield
        finally:
            self.exit_function_call()

    def enter_function_call(self, function_callable: CallableFunction, arguments: list[SLInstanceType]):
        function_name = function_callable.name

        # Check recursion limits
        if function_name in self.recursion_depth:
            self.recursion_depth[function_name] += 1
            if self.recursion_depth[function_name] > self.MAX_RECURSION_DEPTH:
                raise SLRecursionError(f"Exceeded maximum recursion depth in function '{function_name}'")
        else:
            self.recursion_depth[function_name] = 1

        # Create a new symbol table for the function scope
        function_symbol_table = SymbolTable(parent=self.current_symbol_table, is_restricted=True)
        self.current_symbol_table = function_symbol_table

        #Get SLTypes for each argument
        arg_types = [arg.type_descriptor for arg in arguments]
        # Assign arguments to the function parameters
        for param, arg, t in zip(function_callable.parameters, arguments, arg_types):
            self.current_symbol_table.declare(param.name, t=t, value=arg)

        # Push a detailed call frame onto the call stack
        call_frame = CallFrame(function_name, arguments, self.current_symbol_table)
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

    def execute_function(self, function_name: str, arguments: list[ParserNode]):
        try:
            # Evaluate arguments
            evaluated_arguments = [arg.evaluate(self) for arg in arguments]

            # Lookup the function
            func_callable = self.lookup_function(function_name, evaluated_arguments)
            if func_callable is None:
                raise FunctionNotFoundError(f"Function '{function_name}' not found")

            # Invoke the function; context management is handled within the callable
            return func_callable.implementation.invoke(*evaluated_arguments, context=self)
        except SLException as e:
            raise e

    def get_call_stack_trace(self):
        trace = ""
        for frame in reversed(self.call_stack):
            trace += f"Function '{frame.function_name}' called with arguments {frame.arguments}\n"
        return trace

    def register_builtin_functions(self):
        from StreamLanguage.builtins.functions import PrintFunction
        print_function = PrintFunction()
        self.declare_function(
            identifier='print',
            callable_object=print_function,
            parameters=print_function.parameters,
            return_type=print_function.return_type
        )
