from abc import abstractmethod


class SLType:
    """
    Base class for all SL types (both instance and meta types).
    Contains shared functionality for type manipulation.
    """
    def to_slstring(self):
        raise NotImplementedError("Conversion to SLString not implemented.")

    def to_python_type(self):
        raise NotImplementedError("Conversion to Python native type not implemented.")
