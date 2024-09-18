from enum import IntFlag, Enum

# Define the flags
class BlockFlags(IntFlag):
    ALLOW_FUNCTIONS = 1  # Functions can be declared
    CONTROL_FLOW = 2     # Block is part of control flow (if, loop)
    GLOBAL_SCOPE = 4     # Global scope block
    LOCAL_SCOPE = 8      # Local scope block (within a function)
    CAN_RETURN = 16      # Can contain return statements
    CAN_BREAK = 32       # Can contain break statements
    CAN_CONTINUE = 64    # Can contain continue statements

# Define the block types using the flags
class BlockType(Enum):
    DEFAULT = BlockFlags.LOCAL_SCOPE
    FUNCTION = BlockFlags.ALLOW_FUNCTIONS | BlockFlags.LOCAL_SCOPE | BlockFlags.CAN_RETURN
    IF = BlockFlags.CONTROL_FLOW | BlockFlags.LOCAL_SCOPE
    ELSE = BlockFlags.CONTROL_FLOW | BlockFlags.LOCAL_SCOPE
    LOOP = BlockFlags.CONTROL_FLOW | BlockFlags.LOCAL_SCOPE | BlockFlags.CAN_BREAK | BlockFlags.CAN_CONTINUE
    TRY = BlockFlags.LOCAL_SCOPE
    CATCH = BlockFlags.LOCAL_SCOPE
    FINALLY = BlockFlags.LOCAL_SCOPE
    GLOBAL = BlockFlags.GLOBAL_SCOPE | BlockFlags.ALLOW_FUNCTIONS
    PROGRAM = BlockFlags.GLOBAL_SCOPE | BlockFlags.ALLOW_FUNCTIONS

