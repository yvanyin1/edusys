from enum import Enum

class SessionChangeType(Enum):
    CANCELLED = 0
    POSTPONED = 1
    RESCHEDULED = 2
    CLASSROOM_CHANGE = 3
    