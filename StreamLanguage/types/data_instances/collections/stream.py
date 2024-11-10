from StreamLanguage.types.data_instances.instance_base import SLInstanceType

class SLStream(SLInstanceType):
    type_descriptor = None  # Will be set during registration

    def __init__(self, generator_func, element_type = None):
        if not callable(generator_func):
            raise TypeError("SLStream requires a callable generator function")
        self.generator_func = generator_func
        self.iterator = None
        self.element_type = element_type  # Enforced type hint for stream elements

    def start(self):
        self.iterator = iter(self.generator_func())

    def next(self):
        if not self.iterator:
            self.start()
        try:
            value = next(self.iterator)
            self._validate_type(value)
            return value
        except StopIteration:
            return None  # End of stream

    def _validate_type(self, value):
        if not isinstance(value, self.element_type.python_type):
            raise TypeError(f"Stream element expected to be of type {self.element_type}, got {type(value)}")

    def map(self, func):
        # func should accept an argument of type element_type and return a value
        def mapped_generator():
            for item in self:
                self._validate_type(item)
                result = func(item)
                yield result
        # Return a new SLStream with possibly a different element type
        return SLStream(mapped_generator, element_type=func.return_type)

    def filter(self, predicate):
        # predicate should accept an argument of type element_type and return a bool
        def filtered_generator():
            for item in self:
                self._validate_type(item)
                if predicate(item):
                    yield item
        # Return a new SLStream with the same element type
        return SLStream(filtered_generator, element_type=self.element_type)

    def reduce(self, reducer, initial=None):
        # reducer should accept two arguments: accumulator and current item
        from functools import reduce
        self.start()
        if initial is not None:
            return reduce(reducer, self.iterator, initial)
        else:
            return reduce(reducer, self.iterator)

    def to_slstring(self):
        from StreamLanguage.types.data_instances.primatives.string import SLString
        return SLString("<stream object>")

    def __str__(self):
        return "<stream object>"

    def __iter__(self):
        if not self.iterator:
            self.start()
        return self.iterator