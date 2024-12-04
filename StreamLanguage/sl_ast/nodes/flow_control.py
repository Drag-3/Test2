import uuid

from StreamLanguage.sl_ast.nodes.base import ParserNode
from StreamLanguage.sl_ast.exceptions import ParserError
from StreamLanguage.sl_ast.block_types import BlockType
from StreamLanguage.exceptions import SLException
from StreamLanguage.interpreter.contextN import Context


class IfNode(ParserNode):
    """
    A node that represents an if statement.
    """

    BlockType = BlockType.IF

    def __init__(self, condition: ParserNode, then_block: list[ParserNode], else_block:list[ParserNode] | None = None):
        super().__init__('if')
        self.condition = condition
        self.then_block_uuid = str(uuid.uuid4())
        self.else_block_uuid = str(uuid.uuid4()) if else_block else None
        self.then_block = then_block
        self.else_block = else_block

    def children(self) -> list:
        children = [self.condition] + self.then_block
        if self.else_block:
            children += self.else_block
        return children

    def evaluate(self, context: Context):
        try:
            if self.condition.evaluate(context):
                with context.block_context(BlockType.IF, self.then_block_uuid):
                    for node in self.then_block:
                        node.evaluate(context)
                        # Check for control flow signals
                        if context.control_flow.should_return or context.control_flow.should_break or context.control_flow.should_continue:
                            break  # Stop evaluating further nodes
            elif self.else_block:
                with context.block_context(BlockType.IF, self.else_block_uuid):
                    for node in self.else_block:
                        node.evaluate(context)
                        # Check for control flow signals
                        if context.control_flow.should_return or context.control_flow.should_break or context.control_flow.should_continue:
                            break  # Stop evaluating further nodes
            # No need to return a value; control flow is managed via ControlFlowManager
        except SLException as e:
            self.handle_error(e, context)

    def get_type(self, context: Context):
        try:
            then_type = self.then_block[0].get_type(context) if self.then_block else None
            else_type = self.else_block[0].get_type(context) if self.else_block else None
            if then_type and else_type and then_type != else_type:
                raise ParserError("Type mismatch between then and else branches", node=self)
            return then_type or else_type
        except SLException as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        block_info = f" in then_block UUID {self.then_block_uuid}"
        if self.else_block and context.blocks_stack and context.blocks_stack[-1] == self.else_block_uuid:
            block_info = f" in else_block UUID {self.else_block_uuid}"
        error_message = f"Error{block_info}: {str(error)}"
        raise ParserError(error_message, node=self)




class WhileNode(ParserNode):
    """
    A node that represents a while loop.
    """

    BlockType = BlockType.LOOP

    def __init__(self, condition: ParserNode, body: list[ParserNode]):
        super().__init__('while')
        self.condition = condition
        self.body_uuid = str(uuid.uuid4())
        self.body = body

    def children(self):
        return [self.condition] + self.body

    def evaluate(self, context):
        try:
            with context.block_context(BlockType.LOOP, self.body_uuid):
                while self.condition.evaluate(context):
                    for node in self.body:
                        node.evaluate(context)
                        # Check for control flow signals
                        if context.control_flow.should_return:
                            # Propagate the return signal upwards
                            return
                        if context.control_flow.should_break:
                            # Reset the break signal and exit the loop
                            context.control_flow.should_break = False
                            return
                        if context.control_flow.should_continue:
                            # Reset the continue signal and proceed to next iteration
                            context.control_flow.should_continue = False
                            break  # Break out of body loop to re-evaluate condition
        except SLException as e:
            self.handle_error(e, context)

    def get_type(self, context):
        try:
            condition_type = self.condition.get_type(context)
            if condition_type != bool:
                raise ParserError("While loop condition must be a boolean", node=self)
            for node in self.body:
                node.get_type(context)
            return None
        except SLException as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in while loop body UUID {self.body_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)


class ForNode(ParserNode):
    """
    A node that represents a for loop.
    """

    BlockType = BlockType.LOOP

    def __init__(self, initializer: ParserNode, condition: ParserNode, increment: ParserNode, body: list[ParserNode]):
        super().__init__('for')
        self.initializer = initializer
        self.condition = condition
        self.increment = increment
        self.body_uuid = str(uuid.uuid4())
        self.body = body

    def children(self):
        return [self.initializer, self.condition, self.increment] + self.body

    def evaluate(self, context):
        try:
            with context.block_context(BlockType.LOOP, self.body_uuid):
                self.initializer.evaluate(context)
                while self.condition.evaluate(context):
                    for node in self.body:
                        node.evaluate(context)
                        # Check for control flow signals
                        if context.control_flow.should_return:
                            # Propagate the return signal upwards
                            return
                        if context.control_flow.should_break:
                            # Reset the break signal and exit the loop
                            context.control_flow.should_break = False
                            return
                        if context.control_flow.should_continue:
                            # Reset the continue signal and proceed to increment and next iteration
                            context.control_flow.should_continue = False
                            break  # Break out to increment and re-evaluate condition
                    self.increment.evaluate(context)
        except SLException as e:
            self.handle_error(e, context)

    def get_type(self, context):
        try:
            self.initializer.get_type(context)
            condition_type = self.condition.get_type(context)
            if condition_type != bool:
                raise ParserError("For loop condition must be a boolean", node=self)
            self.increment.get_type(context)
            for node in self.body:
                node.get_type(context)
            return None
        except SLException as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in for loop body UUID {self.body_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)


class BreakNode(ParserNode):
    """
    A node that represents a break statement.
    """

    def __init__(self):
        super().__init__('break')

    def evaluate(self, context):
        # Set the break signal in the control flow manager
        context.control_flow.set_break()
        # Return immediately
        return

    def get_type(self, context):
        return None  # Break statements do not have a type

    def handle_error(self, error, context):
        error_message = f"Error in break statement: {str(error)}"
        raise ParserError(error_message, node=self)

class ContinueNode(ParserNode):
    """
    A node that represents a continue statement.
    """

    def __init__(self):
        super().__init__('continue')

    def evaluate(self, context):
        # Set the continue signal in the control flow manager
        context.control_flow.set_continue()
        # Return immediately
        return

    def get_type(self, context):
        return None  # Continue statements do not have a type

    def handle_error(self, error, context):
        error_message = f"Error in continue statement: {str(error)}"
        raise ParserError(error_message, node=self)
