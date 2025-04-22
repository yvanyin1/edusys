from enum import Enum

class RequestStatus(Enum):
    DRAFT = 1
    SUBMITTED = 2
    REQUIRES_CHANGES = 3
    CANCELLED = 4
    PROCESSED = 5