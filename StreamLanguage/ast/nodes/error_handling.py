import uuid

from StreamLanguage.ast.block_types import BlockType, BlockFlags
from StreamLanguage.ast.nodes.base import ParserNode
from StreamLanguage.ast.nodes.functions import ReturnNode
from StreamLanguage.ast.exceptions import ReturnException, ParserError
from StreamLanguage.exceptions import SLException




class TryCatchNode(ParserNode):
    BLOCK_TYPE = BlockType.TRY
    def __init__(self, try_block, catch_clauses, finally_block=None):
        super().__init__('try_catch')
        self.try_block = try_block
        self.catch_clauses = catch_clauses  # List of tuples (exception_var, exception_type, handler_block)
        self.finally_block = finally_block

    def set_block_types(self, context):
        # Set block type for the try block
        context.enter_block(self.block_uuid, BlockType.TRY)

        # Set block type for the catch block if it exists
        if self.catch_clauses:
            context.enter_block(str(uuid.uuid4()), BlockType.CATCH)

        # Set block type for the finally block if it exists
        if self.finally_block:
            context.enter_block(str(uuid.uuid4()), BlockType.FINALLY)


    def children(self):
        nodes = self.try_block
        for _, _, handler_block in self.catch_clauses:
            nodes += handler_block
        if self.finally_block:
            nodes += self.finally_block
        return nodes

    def evaluate(self, context):
        exception_caught = False
        try:
            with context.block_context(BlockType.TRY, self.block_uuid):
                for node in self.try_block:
                    node.evaluate(context)
                    # Check for control flow signals
                    if (context.control_flow.should_return or context.control_flow.should_break or
                            context.control_flow.should_continue or context.control_flow.should_raise):
                        break
        except SLException as e:
            # Should not occur; exceptions are handled via control flow manager
            self.handle_error(e, context)
        finally:
            if context.control_flow.should_raise and not exception_caught:
                exception = context.control_flow.exception
                # Attempt to handle the exception in the catch clauses
                handled = False
                for exception_var, exception_type, handler_block in self.catch_clauses:
                    if self.exception_matches(exception, exception_type):
                        handled = True
                        exception_caught = True
                        with context.block_context(BlockType.CATCH, str(uuid.uuid4())):
                            # Bind the exception to a variable in the catch block
                            if exception_var:
                                context.declare_variable(exception_var, t=exception.type_descriptor, v=exception)
                            for node in handler_block:
                                node.evaluate(context)
                                # Check for control flow signals
                                if (context.control_flow.should_return or context.control_flow.should_break or
                                        context.control_flow.should_continue or context.control_flow.should_raise):
                                    break
                        # Reset the exception signal since it's been handled
                        context.control_flow.should_raise = False
                        context.control_flow.exception = None
                        break
                if not handled:
                    # If not handled, propagate the exception upwards
                    return
            # Always execute the finally block if it exists
            if self.finally_block:
                with context.block_context(BlockType.FINALLY, str(uuid.uuid4())):
                    for node in self.finally_block:
                        node.evaluate(context)
                        # Check for control flow signals
                        if (context.control_flow.should_return or context.control_flow.should_break or
                                context.control_flow.should_continue or context.control_flow.should_raise):
                            break

    def exception_matches(self, exception_instance, exception_type):
        """
        Check if the exception instance's type matches the given exception type.
        """
        return exception_instance.type_descriptor.is_subtype_of(exception_type)

    def get_type(self, context):
        try:
            context.enter_block(self.block_uuid, BlockType.TRY)
            for node in self.try_block:
                node.get_type(context)
            if self.catch_block:
                exception_type, handler_block = self.catch_block
                context.enter_block(str(uuid.uuid4()), BlockType.CATCH)  # Enter catch block
                for node in handler_block:
                    node.get_type(context)
                context.exit_block()
            if self.finally_block:
                context.enter_block(str(uuid.uuid4()), BlockType.FINALLY)  # Enter finally block
                for node in self.finally_block:
                    node.get_type(context)
                context.exit_block()
        except SLException as e:
            self.handle_error(e, context)
        finally:
            context.exit_block()


class ThrowNode(ParserNode):
    def __init__(self, exception_expression):
        super().__init__('throw')
        self.exception_expression = exception_expression

    def children(self):
        return [self.exception_expression]

    def evaluate(self, context):
        exception_instance = self.exception_expression.evaluate(context)
        # Set the exception signal in the control flow manager
        context.control_flow.set_exception(exception_instance)
        return

    def get_type(self, context):
        return None  # Throw statement does not return a value

    def handle_error(self, error, context):
        error_message = f"Error in throw statement: {str(error)}"
        raise ParserError(error_message, node=self)
