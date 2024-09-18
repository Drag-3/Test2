from StreamLanguage.types.base import SLType
from StreamLanguage.types.meta_type.collections.array_type import SLArrayType
from StreamLanguage.types.data_instances.primatives.string import SLString

class SLArray(SLType):
    type_descriptor = SLArrayType()

    def __init__(self, value):
        if not isinstance(value, list):
            raise TypeError("SLArray requires a list")
        self.value = value

    def to_slstring(self):
        return SLString(str(self.value))

    def to_python_type(self):
        return self.value

    @classmethod
    def from_elements(cls, *args):
        """ Create an SLArray from multiple arguments """
        return cls(args)

    @classmethod
    def from_range(cls, start, end, step=1):
        """ Create an SLArray from a range of numbers """
        return cls(range(start, end, step))

    def append(self, value):
        """ Append a value to the end of the array """
        self.value.append(value)

    def get(self, index):
        """ Get the value at the given index """
        return self.value[index]

    def insert(self, index, value):
        """ Insert a value at the given index """
        self.value.insert(index, value)

    def slice(self, start=None, end=None, step=None):
        """ Return a slice of the array as a new SLArray """
        sliced = self.value[start:end:step]
        return SLArray(sliced)

    def map(self, func):
        """ Apply a function to all elements of the array and return a new SLArray """
        if not callable(func):
            raise TypeError("func must be callable")
        mapped = [func(x) for x in self.value]
        return SLArray(mapped)

    def filter(self, func):
        """ Filter the array by a function and return a new SLArray """
        if not callable(func):
            raise TypeError("func must be callable")
        filtered = [x for x in self.value if func(x)]
        return SLArray(filtered)

    def pop(self, index=-1):
        try:
            return self.value.pop(index)
        except IndexError:
            raise IndexError("pop index out of range")

    def remove(self, value):
        """ Remove the first occurance of the value """
        self.value.remove(value)

    def reverse(self):
        """ Reverse the array """
        self.value.reverse()

    def sort(self):
        """ Sort the array """
        self.value.sort()

    def clear(self):
        """ Clear the array """
        self.value.clear()

    def copy(self):
        """ Return a shallow copy of the array """
        return SLArray(self.value.copy())

    def count(self, value):
        """ Return the number of occurances of the value """
        return self.value.count(value)

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        if isinstance(other, SLArray):
            return SLArray(self.value + other.value)
        return NotImplemented

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, value):
        self.value[key] = value

    def __delitem__(self, key):
        del self.value[key]

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value)

    def __contains__(self, item):
        return item in self.value

    def __repr__(self):
        return f"SLArray({self.value})"

