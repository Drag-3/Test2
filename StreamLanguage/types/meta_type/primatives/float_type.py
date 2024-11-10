from StreamLanguage.types.meta_type.meta_base import SLMetaType

class SLFloatType(SLMetaType):
    """
    Represents the float type in StreamLanguage.
    """

    def __init__(self):
        super().__init__("Float")

    def __str__(self):
        return "Float"