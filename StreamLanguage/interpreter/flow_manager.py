class ControlFlowManager:

    def __init__(self):
        self.reset()

    def reset(self):
        self.should_return = False
        self.return_value = None
        self.return_metadata = None
        self.should_break = False
        self.break_metadata = None  #
        self.should_continue = False
        self.continue_metadata = None

        self.should_raise = False
        self.exception = None
        self.exception_metadata = None


    def set_return(self, value, metadata=None):
        self.should_return = True
        self.return_value = value
        self.return_metadata = metadata

    def set_break(self, metadata=None):
        self.should_break = True
        self.break_metadata = metadata

    def set_continue(self, metadata=None):
        self.should_continue = True
        self.continue_metadata = metadata

    def set_exception(self, exception, metadata=None):
        self.should_raise = True
        self.exception = exception
        self.exception_metadata = metadata


    def dump(self):
        return {
            'should_return': self.should_return,
            'return_value': self.return_value,
            'return_metadata': self.return_metadata,
            'should_break': self.should_break,
            'break_metadata': self.break_metadata,
            'should_continue': self.should_continue,
            'continue_metadata': self.continue_metadata,
            'should_raise': self.should_raise,
            'exception': self.exception,
            'exception_metadata': self.exception_metadata
        }