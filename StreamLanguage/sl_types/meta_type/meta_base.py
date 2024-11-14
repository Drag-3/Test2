from  StreamLanguage.sl_types.base import SLType

class SLMetaType(SLType):
    """
       Base class for all SL meta sl_types (e.g., SLIntegerType).
       Responsible for metadata and type introspection.
       """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"MetaType: {self.name}"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
