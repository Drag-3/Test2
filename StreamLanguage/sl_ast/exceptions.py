"""
Exceptions and Signals for the AST module.
"""
from StreamLanguage.exceptions import SLException, SLBaseException


class ParserError(SLException):
    def __init__(self, message, node=None):
        super().__init__(message)
        self.node = node
        if node:
            # Assuming node has token with line and column or similar identifiers
            self.message = f"Error at line : {message}"
        else:
            self.message = message

    def __str__(self):
        return self.message

class VariableNotDeclaredError(ParserError):
    def __init__(self, message):
        super().__init__(message)

class VariableRedeclaredError(ParserError):
    def __init__(self, message):
        super().__init__(message)

class FunctionDeclarationError(ParserError):
    def __init__(self, message):
        super().__init__(message)

class FunctionNotFoundError(ParserError):
    def __init__(self, message):
        super().__init__(message)

class SLRecursionError(ParserError):
    def __init__(self, message):
        super().__init__(message)

class SLTypeError(ParserError):
    def __init__(self, message):
        super().__init__(message)

class SLValueError(ParserError):
    def __init__(self, message):
        super().__init__(message)

class SLIndexError(ParserError):
    def __init__(self, message):
        super().__init__(message)

class SLKeyError(ParserError):
    def __init__(self, message):
        super().__init__(message)

class InvalidOperationError(ParserError):
    def __init__(self, message):
        super().__init__(message)


class ReturnException(SLBaseException):
    def __init__(self, value):
        self.value = value

class BreakException(SLException):
    pass

class ContinueException(SLException):
    pass
