from abc import abstractmethod


class SLType:
    """
    Base class for all types in StreamLanguage.
    """

    @abstractmethod
    def to_slstring(self):

        """
        Converts the type instance to an SLString instance.
        """
        pass

    @abstractmethod
    def to_python_type(self):
        """
        Converts the type instance to the closest native Python type.
        This method must be overridden by all subclasses to ensure proper conversion.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def __str__(self):
        """
        Returns the string representation of the type, which should be overridden by all subclasses.
        """
        return f"<{self.__class__.__name__}>"

    def __eq__(self, other):
        """
        Checks equality between this object and another SLType object.
        """
        if isinstance(other, SLType):
            return self.to_python_type() == other.to_python_type()
        return False

    def __repr__(self):
        """
        Official string representation of the type.
        """
        return self.__str__()
