from StreamLanguage.sl_types.meta_type.meta_base import SLMetaType

class SLBooleanType(SLMetaType):
    """
    Represents the boolean type in StreamLanguage.
    """

    def __init__(self):
        super().__init__("Boolean")

    def __str__(self):
        return "Boolean"