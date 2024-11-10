from  StreamLanguage.types.base import SLType

class SLMetaType(SLType):
    """
       Base class for all SL meta types (e.g., SLIntegerType).
       Responsible for metadata and type introspection.
       """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"MetaType: {self.name}"