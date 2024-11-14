from abc import abstractmethod


class SLType:
    """
    Base class for all SL sl_types (both instance and meta sl_types).
    Contains shared functionality for type manipulation.
    """
    def to_slstring(self):
        raise NotImplementedError("Conversion to SLString not implemented.")

    def to_python_type(self):
        raise NotImplementedError("Conversion to Python native type not implemented.")
