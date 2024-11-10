from StreamLanguage.ast.block_types import BlockFlags
from StreamLanguage.interpreter.symbol_table import SymbolTable


class Block:
    def __init__(self, block_type):
        self.block_type = block_type
        self.symbol_table = SymbolTable()
        # Additional attributes as needed

    def can_define_function(self):
        return (self.block_type.value & BlockFlags.ALLOW_FUNCTIONS) != 0