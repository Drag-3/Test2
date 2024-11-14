from StreamLanguage.sl_types.data_instances.instance_base import SLInstanceType

class SLQueue(SLInstanceType):
    """
    Represents a queue in StreamLanguage.
    """
    type_descriptor = None  # Will be attached during registration

    def __init__(self, value=None):
        if isinstance(value, SLQueue):
            self.value = value.value
        elif isinstance(value, list):
            self.value = value
        else:
            raise TypeError("SLQueue requires a list or another SLQueue")

    def enqueue(self, element):
        self.value.append(element)

    def dequeue(self):
        if not self.value:
            raise IndexError("Queue is empty")
        return self.value.pop(0)

    def to_slstring(self):
        from StreamLanguage.sl_types.data_instances.primatives.string import SLString
        return SLString(str(self.value))

    def __str__(self):
        return str(self.value)

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value)