# builtins.py
from StreamLanguage.sl_ast.callables import Callable
from StreamLanguage.sl_ast.exceptions import SLTypeError
from StreamLanguage.sl_ast.nodes.expressions import IdentifierNode
from StreamLanguage.exceptions import SLException
from StreamLanguage.sl_types.data_instances.primatives.boolean import SLBoolean
from StreamLanguage.sl_types.data_instances.primatives.float import SLFloat
from StreamLanguage.sl_types.data_instances.primatives.integer import SLInteger
from StreamLanguage.sl_types.data_instances.primatives.string import SLString
from StreamLanguage.sl_types.meta_type.meta_base import SLMetaType
from StreamLanguage.sl_types.meta_type.primatives.integer_type import SLIntegerType
from StreamLanguage.sl_types.meta_type.primatives.string_type import SLStringType


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


class ReadIntFunction(Callable):
    def __init__(self):
        """
        Initialize the ReadIntFunction.
        Does not accept any arguments.
        Returns an integer.
        """
        super().__init__(return_type=SLIntegerType, arg_types=[])
        self.name = 'read_int'
        self.parameters = []  # No parameters

    def invoke(self, context):
        """
        Read an integer from the user input.

        :param context: The current execution context.
        :return: The integer read from input.
        """
        try:
            user_input = input()
            value = SLInteger(int(user_input))
            return value
        except ValueError:
            raise SLTypeError(f"Invalid integer input: '{user_input}'")
        except Exception as e:
            raise SLException(f"Error in read_int function: {str(e)}")


class ReadStringFunction(Callable):
    def __init__(self):
        """
        Initialize the ReadStringFunction.
        Does not accept any arguments.
        Returns a string.
        """
        super().__init__(return_type=SLStringType, arg_types=[])
        self.name = 'read_string'
        self.parameters = []  # No parameters

    def invoke(self, context):
        """
        Read a string from the user input.

        :param context: The current execution context.
        :return: The string read from input.
        """
        try:
            user_input = SLString(input())
            return user_input
        except Exception as e:
            raise SLException(f"Error in read_string function: {str(e)}")


# builtins.py (continued)

class ReadDataFunction(Callable):
    def __init__(self):
        """
        Initialize the ReadDataFunction.
        Does not accept any arguments.
        Returns data of type int, float, bool, or str based on input.
        """
        super().__init__(return_type=SLMetaType, arg_types=[])
        self.name = 'read_data'
        self.parameters = []  # No parameters

    def invoke(self, context):
        """
        Read data from the user input and determine its type.

        :param context: The current execution context.
        :return: The data read from input with appropriate type.
        """
        try:
            user_input = input().strip()

            # Try to parse as integer
            try:
                return SLInteger(int(user_input))
            except ValueError:
                pass

            # Try to parse as float
            try:
                return SLFloat(float(user_input))
            except ValueError:
                pass

            # Check for boolean
            if user_input.lower() in ['true', 'false']:
                return SLBoolean(user_input.lower() == 'true')

            # Default to string
            return SLString(user_input)

        except Exception as e:
            raise SLException(f"Error in read_data function: {str(e)}")
