from StreamLanguage.types.meta_type.meta_base import SLMetaType

class SLArrayType(SLMetaType):
    """
    Represents the array type in StreamLanguage.
    """

    def __init__(self, element_type):
        super().__init__("Array")
        self.element_type = element_type

    def __str__(self):
        return f"Array<{self.element_type}>"