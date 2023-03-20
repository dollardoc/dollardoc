from enum import Enum


class InputFormatType(Enum):
    TEXT = 0
    DOLLAR_OBJECT = 1
    DOLLAR_OBJECT_VALUE = 2
    FUNCTION = 3
    BLOCK = 4
    UNION = 5
