from StreamLanguage.types.data_instances.instance_base import SLInstanceType

class SLArray(SLInstanceType):
    """
    Represents an array in StreamLanguage.
    """
    type_descriptor = None  # Will be attached during registration

    def __init__(self, value=None):
        if isinstance(value, SLArray):
            self.value = value.value
        elif isinstance(value, list):
            self.value = value
        else:
            raise TypeError("SLArray requires a list or another SLArray")

    def append(self, element):
        self.value.append(element)

    def get(self, index):
        return self.value[index]

    def slice(self, start, end):
        return self.value[start:end]



    def to_slstring(self):
        from StreamLanguage.types.data_instances.primatives.string import SLString
        return SLString(str(self.value))

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        if isinstance(other, SLArray):
            return SLArray(self.value + other.value)
        return NotImplemented

    def __getitem__(self, key):
        return self.value[key]

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value)