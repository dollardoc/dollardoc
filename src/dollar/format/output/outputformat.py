from typing import List

from dollar.dollarexecutionexception import DollarExecutionException
from dollar.dollarobject import DollarObject
from dollar.format.output.outputformattype import OutputFormatType


class _OutputFormat:

    def __init__(self, format_type: OutputFormatType, children: List['_OutputFormat']):
        self.format_type = format_type
        self.children = children
        self.allowed_children = []

    def getformattype(self):
        return self.format_type

    def getchildren(self):
        return self.children

    def isblock(self):
        return False

    def validate(self):
        for child in self.children:
            if child.getformattype() not in self.allowed_children:
                raise DollarExecutionException(
                    "{} is not allowed in {}".format(child.getformattype(), self.getformattype()))


class _OutputFormatBlock(_OutputFormat):

    def __init__(self, format_type: OutputFormatType, children: List[_OutputFormat]):
        self.format_type = format_type
        self.children = children
        self.allowed_children = []

    def isblock(self):
        return True


class OutputFormatText(_OutputFormat):

    def __init__(self, text):
        self.format_type = OutputFormatType.TEXT
        self.text = text
        self.children = []

    def gettext(self):
        return self.text

    def validate(self):
        if "\n" in self.text:
            raise DollarExecutionException(
                "{} is not allowed to contain newline".format(self.getformattype()))


class OutputFormatBold(_OutputFormat):

    def __init__(self, children: List[_OutputFormat]):
        self.format_type = OutputFormatType.BOLD
        self.children = children
        self.allowed_children = [
            OutputFormatType.TEXT,
            OutputFormatType.ITALIC,
            OutputFormatType.LINK,
            OutputFormatType.DOLLAR_OBJECT,
        ]


class OutputFormatItalic(_OutputFormat):

    def __init__(self, children: List[_OutputFormat]):
        self.format_type = OutputFormatType.ITALIC
        self.children = children
        self.allowed_children = [
            OutputFormatType.TEXT,
            OutputFormatType.BOLD,
            OutputFormatType.LINK,
            OutputFormatType.DOLLAR_OBJECT,
        ]


class OutputFormatCode(OutputFormatText):

    def __init__(self, text):
        self.format_type = OutputFormatType.CODE
        self.text = text
        self.children = []


class OutputFormatLink(_OutputFormat):

    def __init__(self, href: str, children: List[_OutputFormat]):
        self.format_type = OutputFormatType.LINK
        self.children = children
        self.href = href
        self.allowed_children = [
            OutputFormatType.TEXT,
            OutputFormatType.BOLD,
            OutputFormatType.ITALIC
        ]

    def gethref(self):
        return self.href


class OutputFormatHeader(_OutputFormatBlock):

    def __init__(self, level: int, children: List[_OutputFormat]):
        self.format_type = OutputFormatType.HEADER
        self.children = children
        self.level = level
        self.allowed_children = [
            OutputFormatType.TEXT,
            OutputFormatType.BOLD,
            OutputFormatType.ITALIC,
            OutputFormatType.LINK,
            OutputFormatType.DOLLAR_OBJECT,
            OutputFormatType.CODE,
        ]

    def getlevel(self):
        return self.level


class OutputFormatParagraph(_OutputFormatBlock):

    def __init__(self, children: List[_OutputFormat]):
        self.format_type = OutputFormatType.PARAGRAPH
        self.children = children
        self.allowed_children = [
            OutputFormatType.TEXT,
            OutputFormatType.BOLD,
            OutputFormatType.ITALIC,
            OutputFormatType.LINK,
            OutputFormatType.DOLLAR_OBJECT,
            OutputFormatType.CODE,
        ]


class OutputFormatOrderedList(_OutputFormatBlock):

    def __init__(self, children: List[_OutputFormat]):
        self.format_type = OutputFormatType.ORDERED_LIST
        self.children = children
        self.allowed_children = [
            OutputFormatType.LIST_ITEM,
            OutputFormatType.ORDERED_LIST,
            OutputFormatType.UNORDERED_LIST,
        ]


class OutputFormatUnorderedList(_OutputFormatBlock):

    def __init__(self, children: List[_OutputFormat]):
        self.format_type = OutputFormatType.UNORDERED_LIST
        self.children = children
        self.allowed_children = [
            OutputFormatType.LIST_ITEM,
            OutputFormatType.ORDERED_LIST,
            OutputFormatType.UNORDERED_LIST,
        ]


class OutputFormatListItem(_OutputFormatBlock):

    def __init__(self, children: List[_OutputFormat]):
        self.format_type = OutputFormatType.LIST_ITEM
        self.children = children
        self.allowed_children = [
            OutputFormatType.TEXT,
            OutputFormatType.BOLD,
            OutputFormatType.ITALIC,
            OutputFormatType.LINK,
            OutputFormatType.DOLLAR_OBJECT,
            OutputFormatType.CODE,
        ]


class OutputFormatCodeBlock(_OutputFormatBlock):

    def __init__(self, code_type, text):
        self.format_type = OutputFormatType.CODE_BLOCK
        self.code_type = code_type
        self.text = text
        self.children = []

    def getcodetype(self):
        return self.code_type

    def gettext(self):
        return self.text


class OutputFormatQuoteBlock(_OutputFormatBlock):

    def __init__(self, children: List[_OutputFormat]):
        self.format_type = OutputFormatType.QUOTE_BLOCK
        self.children = children
        self.allowed_children = [
            OutputFormatType.HEADER,
            OutputFormatType.PARAGRAPH,
            OutputFormatType.ORDERED_LIST,
            OutputFormatType.UNORDERED_LIST,
            OutputFormatType.CODE_BLOCK,
            OutputFormatType.QUOTE_BLOCK,
        ]


class OutputFormatDefinition(_OutputFormatBlock):

    def __init__(self, defined_children: List[_OutputFormat], definition_children: List[_OutputFormat]):
        self.format_type = OutputFormatType.DEFINITION
        self.defined_children = defined_children
        self.definition_children = definition_children
        self.allowed_children = [
            OutputFormatType.TEXT,
            OutputFormatType.BOLD,
            OutputFormatType.ITALIC,
            OutputFormatType.LINK,
            OutputFormatType.DOLLAR_OBJECT,
            OutputFormatType.CODE,
        ]

    def getdefinedchildren(self):
        return self.defined_children

    def getdefinitionchildren(self):
        return self.definition_children

    def validate(self):
        for child in self.defined_children:
            if child.getformattype() not in self.allowed_children:
                raise DollarExecutionException(
                    "{} is not allowed in {}".format(child.getformattype(), self.getformattype()))
        for child in self.definition_children:
            if child.getformattype() not in self.allowed_children:
                raise DollarExecutionException(
                    "{} is not allowed in {}".format(child.getformattype(), self.getformattype()))


class OutputFormatPluginBlock(_OutputFormatBlock):

    def __init__(self, plugin_name, text):
        self.format_type = OutputFormatType.PLUGIN_BLOCK
        self.plugin_name = plugin_name
        self.text = text
        self.children = []

    def getpluginname(self):
        return self.plugin_name

    def gettext(self):
        return self.text


class OutputFormatDollarObject(_OutputFormat):

    def __init__(self, dollar_object: DollarObject):
        self.format_type = OutputFormatType.DOLLAR_OBJECT
        self.children = []
        self.dollar_object = dollar_object
        self.allowed_children = []

    def getdollarobject(self) -> DollarObject:
        return self.dollar_object

    def gethref(self, this_dollar_object) -> str:
        fr = this_dollar_object.gettargetpath().split("/")
        to = self.dollar_object.gettargetpath().split("/")
        length = len(fr)
        if length > len(to):
            length = len(to)
        for i in range(0, length-1):
            if fr[0] == to[0]:
                fr = fr[1:]
                to = to[1:]
        result = "/".join(to)
        if len(fr) > 1:
            result = (len(fr)-1) * "../" + result
        else:
            result = "./" + result
        return result


