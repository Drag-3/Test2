from StreamLanguage.types.meta_type.meta_base import SLMetaType

class SLQueueType(SLMetaType):
    """
    Represents the queue type in StreamLanguage.
    """

    def __init__(self):
        super().__init__("Queue")

    def __str__(self):
        return "Queue"