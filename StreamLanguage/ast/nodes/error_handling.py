import uuid

from StreamLanguage.ast.block_types import BlockType, BlockFlags
from StreamLanguage.ast.nodes.base import ParserNode
from StreamLanguage.ast.nodes.functions import ReturnNode
from StreamLanguage.ast.exceptions import ReturnException
from StreamLanguage.exceptions import SLException




class TryCatchNode(ParserNode):
    BLOCK_TYPE = BlockType.TRY
    def __init__(self, try_block, catch_block, finally_block=None):
        super().__init__('try_catch')
        self.try_block = try_block        # List of ParserNodes for the try block
        self.catch_block = catch_block    # Tuple (exception_type, handler_block)
        self.finally_block = finally_block  # List of ParserNodes for the finally block
        self.block_uuid = str(uuid.uuid4())  # Unique identifier for this block

    def set_block_types(self, context):
        # Set block type for the try block
        context.enter_block(self.block_uuid, BlockType.TRY)

        # Set block type for the catch block if it exists
        if self.catch_block:
            context.enter_block(str(uuid.uuid4()), BlockType.CATCH)

        # Set block type for the finally block if it exists
        if self.finally_block:
            context.enter_block(str(uuid.uuid4()), BlockType.FINALLY)


    def children(self):
        nodes = self.try_block + [self.catch_block[1]]
        if self.finally_block:
            nodes += self.finally_block
        return nodes

    def evaluate(self, context):
        return_value = None
        try:
            # Handle the try block
            context.enter_try()
            for node in self.try_block:
                return_value = node.evaluate(context)
                if isinstance(node, ReturnNode):
                    break
            context.exit_block()
        except SLException as e:
            # Handle the catch block if the exception matches
            if self.catch_block and isinstance(e, self.catch_block[0]):
                exception_type, handler_block = self.catch_block
                context.enter_catch(e)
                for node in handler_block:
                    return_value = node.evaluate(context)
                    if isinstance(node, ReturnNode):
                        break
                context.exit_block()
            else:
                raise  # Re-raise the exception if not handled here
        finally:
            # Handle the finally block
            if self.finally_block:
                context.enter_finally()
                for node in self.finally_block:
                    node.evaluate(context)  # Note: Return value of finally is not used
                context.exit_block()

        return return_value

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