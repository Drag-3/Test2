import uuid
from ..exceptions import ParserError

class ParserNode:
    def __init__(self, token, block_uuid=None):
        self.token = token  # The token representing the node in the syntax tree
        self.block_uuid = block_uuid or str(uuid.uuid4())  # Unique identifier for the block

    def children(self) -> list['ParserNode']:
        # Default implementation returns an empty list, override in derived classes
        return []

    def evaluate(self, context):
        raise NotImplementedError("Each node must implement 'evaluate' method for execution.")

    def get_type(self, context):
        raise NotImplementedError("Each node must implement 'get_type' method for type checking.")

    def handle_error(self, error, context):

        error_message = f"Error in block UUID {self.block_uuid}: {str(error)}"
        raise ParserError(error_message, node=self)

    def clone(self) -> 'ParserNode':
        # Utility method to clone the current node
        return ParserNode(self.token, self.block_uuid)

    def get_child_by_type(self, node_type) -> 'ParserNode':
        # Utility method to get the first child of a specific type
        for child in self.children():
            if isinstance(child, node_type):
                return child
        return None

