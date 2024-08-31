import uuid

from .base import ParserNode
from .functions import ReturnNode
from ..exceptions import ReturnException



class TryCatchNode(ParserNode):
    def __init__(self, try_block, catch_block, finally_block=None):
        super().__init__('try_catch')
        self.try_block = try_block        # List of ParserNodes for the try block
        self.catch_block = catch_block    # Tuple (exception_type, handler_block)
        self.finally_block = finally_block  # List of ParserNodes for the finally block
        self.block_uuid = str(uuid.uuid4())  # Unique identifier for this block

    def children(self):
        nodes = self.try_block + [self.catch_block[1]]
        if self.finally_block:
            nodes += self.finally_block
        return nodes

    def evaluate(self, context):
        context.enter_block(self.block_uuid)
        return_value = None
        try:
            for node in self.try_block:
                return_value = node.evaluate(context)
                if isinstance(node, ReturnNode):
                    break
        except ReturnException as re:
            raise re
        except Exception as e:
            if self.catch_block:
                exception_type, handler_block = self.catch_block
                if isinstance(e, exception_type):
                    catch_context = context.clone()
                    context.enter_block(str(uuid.uuid4()))  # New block UUID for the catch block
                    for node in handler_block:
                        return_value = node.evaluate(catch_context)
                        if isinstance(node, ReturnNode):
                            break
                    context.exit_block()
                else:
                    self.handle_error(e, context)
            else:
                self.handle_error(e, context)
        finally:
            if self.finally_block:
                finally_context = context.clone()
                context.enter_block(str(uuid.uuid4()))  # New block UUID for the finally block
                for node in self.finally_block:
                    return_value = node.evaluate(finally_context)
                    if isinstance(node, ReturnNode):
                        break
                context.exit_block()
        context.exit_block()
        return return_value

    def get_type(self, context):
        try:
            context.enter_block(self.block_uuid)
            for node in self.try_block:
                node.get_type(context)
            if self.catch_block:
                exception_type, handler_block = self.catch_block
                context.enter_block(str(uuid.uuid4()))  # New block UUID for the catch block
                for node in handler_block:
                    node.get_type(context)
                context.exit_block()
            if self.finally_block:
                context.enter_block(str(uuid.uuid4()))  # New block UUID for the finally block
                for node in self.finally_block:
                    node.get_type(context)
                context.exit_block()
        except Exception as e:
            self.handle_error(e, context)
        finally:
            context.exit_block()