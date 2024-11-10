from StreamLanguage.types.data_instances.instance_base import SLInstanceType

class SLStack(SLInstanceType):
    type_descriptor = None  # Will be attached during registration

    def __init__(self, value=None):
        if isinstance(value, SLStack):
            self.value = value.value
        elif isinstance(value, list):
            self.value = value
        else:
            raise TypeError("SLStack requires a list or another SLStack")

    def push(self, element):
        self.value.append(element)

    def pop(self):
        if not self.value:
            raise IndexError("Stack is empty")
        return self.value.pop()

    def to_slstring(self):
        from StreamLanguage.types.data_instances.primatives.string import SLString
        return SLString(str(self.value))

    def __str__(self):
        return str(self.value)

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value)