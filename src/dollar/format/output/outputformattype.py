from enum import Enum


class OutputFormatType(Enum):
    TEXT = 0
    BOLD = 1
    ITALIC = 2
    CODE = 3
    LINK = 4
    HEADER = 5
    PARAGRAPH = 6
    TABLE = 7
    TABLE_HEADER = 8
    TABLE_ROW = 9
    ORDERED_LIST = 10
    UNORDERED_LIST = 11
    LIST_ITEM = 12
    CODE_BLOCK = 13
    QUOTE_BLOCK = 14
    DEFINITION = 15
    IMAGE = 16
    PLUGIN_BLOCK = 17
    DOLLAR_OBJECT = 18
