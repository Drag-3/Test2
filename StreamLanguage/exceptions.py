class SLBaseException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message

class SLException(SLBaseException):
    def __init__(self, message: str):
        super().__init__(message)