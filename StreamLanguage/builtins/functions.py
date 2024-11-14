# builtins.py
from StreamLanguage.ast.callables import Callable
from StreamLanguage.ast.nodes.expressions import IdentifierNode
from StreamLanguage.exceptions import SLException


class PrintFunction(Callable):
    def __init__(self):
        """
        Initialize the PrintFunction.
        Accepts a single argument of any type.
        Maybe multiple arguments like python print function later, but I do not know if that would be good for this langauge.
        Later I will extend this to accept multiple keyword arguments. Some might only work with certain types.
        For example, a 'sep' argument might only work with Array types.
        While a padding argument might only work with any type that can be converted to a string.
        """
        super().__init__(return_type=None, arg_types=[])
        self.name = 'print'
        self.parameters = [IdentifierNode("data")]  # Assuming you have a Parameter class

    def invoke(self, data, context):
        """
        Print the value to the console.

        :param data: The value to print (any type).
        :param context: The current execution context.
        :return: None
        """
        try:
            print(data)
            return None
        except Exception as e:
            raise SLException(f"Error in print function: {str(e)}")
