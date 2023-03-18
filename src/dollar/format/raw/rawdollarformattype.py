from enum import Enum


class RawDollarFormatType(Enum):
    TEXT = 0
    REFERENCE = 1
    FUNCTION = 2
    BLOCK = 3
    UNION = 4
