class CallFrame:
    def __init__(self, function_name, arguments, symbol_table):
        self.function_name = function_name
        self.arguments = arguments
        self.symbol_table = symbol_table

    def __repr__(self):
        return f"CallFrame(function_name={self.function_name}, arguments={self.arguments})"
