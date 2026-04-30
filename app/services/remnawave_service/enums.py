from enum import Enum

class UsernameType(str, Enum):
    REGULAR = "user"
    TRIAL = "user"
    TEST = "test"

class ExpireType(str, Enum):
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    THREE_MONTHS = "3MONTH"
    SIX_MONTHS = "6MONTH"
    YEAR = "YEAR"

