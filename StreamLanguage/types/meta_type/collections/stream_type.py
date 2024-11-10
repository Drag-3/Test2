from StreamLanguage.types.meta_type.meta_base import SLMetaType

class SLStreamType(SLMetaType):
    """
    Represents the stream type in StreamLanguage.
    """

    def __init__(self):
        super().__init__("Stream")

    def __str__(self):
        return "Stream"