import uuid

from .base import ParserNode
from ..exceptions import ParserError


class IfNode(ParserNode):
    """
    A node that represents an if statement.
    - `condition`: The condition to evaluate, which determines which branch to execute.
    - `then_block`: The block of code to execute if the condition is true.
    - `else_block`: The block of code to execute if the condition is false (optional).
    """

    def __init__(self, condition, then_block, else_block=None):
        super().__init__('if')
        self.condition = condition
        self.then_block_uuid = str(uuid.uuid4())  # Unique UUID for then_block
        self.else_block_uuid = str(uuid.uuid4()) if else_block else None  # Unique UUID for else_block
        self.then_block = then_block
        self.else_block = else_block

    def children(self) -> list[ParserNode]:
        # Flatten the lists and return all child nodes, including the else block if it exists
        children = [self.condition] + self.then_block
        if self.else_block:
            children += self.else_block
        return children

    def evaluate(self, context):
        try:
            return_val = None
            if self.condition.evaluate(context):
                context.enter_block(self.then_block_uuid)
                for node in self.then_block:
                    return_val = node.evaluate(context)
                context.exit_block()
            elif self.else_block:
                context.enter_block(self.else_block_uuid)
                for node in self.else_block:
                    return_val = node.evaluate(context)
                context.exit_block()
            return return_val
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        """
        The type of an if statement can be ambiguous if the branches return different types,
        hence we check the types of both branches and raise an error if they don't match.
        If the if statement doesn't return anything explicitly, it can be considered as having 'None' type.
        """
        try:
            then_type = self.then_block[0].get_type(context) if self.then_block else None
            else_type = self.else_block[0].get_type(context) if self.else_block else None
            if else_type and then_type != else_type:
                raise ParserError("Type mismatch between then and else branches", node=self)
            return then_type or else_type
        except Exception as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        block_info = f" in then_block UUID {self.then_block_uuid}"
        if self.else_block and context.get_current_block_uuid() == self.else_block_uuid:
            block_info = f" in else_block UUID {self.else_block_uuid}"
        error_message = f"Error{block_info}: {str(error)}"
        raise ParserError(error_message, node=self)



class WhileNode(ParserNode):
    """
    A node that represents a while loop.
    - `condition`: The condition to evaluate for each loop iteration.
    - `body`: The block of code to execute as long as the condition is true.
    """

    def __init__(self, condition, body):
        super().__init__('while')
        self.condition = condition
        self.body_uuid = str(uuid.uuid4())  # Unique UUID for the loop body
        self.body = body  # List of ParserNodes representing the loop body

    def children(self):
        # Flatten and return both the condition and the body nodes
        return [self.condition] + self.body

    def evaluate(self, context):
        """
        Evaluate the while loop within the given context.
        This method repeatedly evaluates the body as long as the condition evaluates to True.
        """
        try:
            context.enter_block(self.body_uuid)  # Enter the loop body block
            while self.condition.evaluate(context):
                for node in self.body:
                    node.evaluate(context)
            context.exit_block()  # Exit the loop body block
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        """
        The while loop will have None type as it doesn't return a value directly.
        """
        try:
            condition_type = self.condition.get_type(context)
            if condition_type != bool:
                raise ParserError("While loop condition must be a boolean", node=self)
            for node in self.body:
                node.get_type(context)
            return None
        except Exception as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in while loop body UUID {self.body_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)

class ForNode(ParserNode):
    def __init__(self, initializer, condition, increment, body):
        super().__init__('for')
        self.initializer = initializer  # Typically an AssignmentNode or VariableDeclarationNode
        self.condition = condition      # Expression node that evaluates to a boolean
        self.increment = increment      # UpdateNode or similar for incrementing/decrementing
        self.body_uuid = str(uuid.uuid4())  # Unique UUID for the loop body
        self.body = body                # List of ParserNodes representing the loop body

    def children(self):
        return [self.initializer, self.condition, self.increment] + self.body

    def evaluate(self, context):
        try:
            self.initializer.evaluate(context)
            context.enter_loop(self.body_uuid)  # Enter the loop
            while self.condition.evaluate(context):
                context.enter_block(self.body_uuid)  # Enter the loop body block
                for statement in self.body:
                    statement.evaluate(context)
                context.exit_block()  # Exit the loop body block
                self.increment.evaluate(context)
            context.exit_loop()  # Exit the loop
        except Exception as e:
            self.handle_error(e, context)

    def get_type(self, context):
        try:
            initializer_type = self.initializer.get_type(context)
            condition_type = self.condition.get_type(context)
            if condition_type != bool:
                raise ParserError("For loop condition must be a boolean", node=self)
            increment_type = self.increment.get_type(context)
            for node in self.body:
                node.get_type(context)
            return None  # For loop itself does not return a value
        except Exception as e:
            self.handle_error(e, context)

    def handle_error(self, error, context):
        error_message = f"Error in for loop body UUID {self.body_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)