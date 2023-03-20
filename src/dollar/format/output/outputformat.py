from typing import List

from dollar.dollarexception import DollarException
from dollar.dollarobject import DollarObject
from dollar.format.output.outputformattype import OutputFormatType


class OutputFormat:

    def __init__(self, format_type: OutputFormatType, children: List['OutputFormat']):
        self.format_type = format_type
        self.children = children
        self.allowed_children = []

    def get_format_type(self):
        return self.format_type

    def get_children(self):
        return self.children

    def is_block(self):
        return False

    def validate(self):
        for child in self.children:
            if child.get_format_type() not in self.allowed_children:
                raise DollarException(
                    "{} is not allowed in {}"
                    .format(child.get_format_type(), self.get_format_type()))


class OutputFormatBlock(OutputFormat):

    def __init__(self, format_type: OutputFormatType, children: List[OutputFormat]):
        super().__init__(format_type, children)

    def is_block(self):
        return True


class OutputFormatText(OutputFormat):

    def __init__(self, text):
        super().__init__(OutputFormatType.TEXT, [])
        self.text = text

    def get_text(self):
        return self.text

    def validate(self):
        if "\n" in self.text:
            raise DollarException(
                "{} is not allowed to contain newline".format(self.get_format_type()))


class OutputFormatBold(OutputFormat):

    def __init__(self, children: List[OutputFormat]):
        super().__init__(OutputFormatType.BOLD, children)
        self.allowed_children = [
            OutputFormatType.TEXT,
            OutputFormatType.ITALIC,
            OutputFormatType.LINK,
            OutputFormatType.DOLLAR_OBJECT,
        ]


class OutputFormatItalic(OutputFormat):

    def __init__(self, children: List[OutputFormat]):
        super().__init__(OutputFormatType.ITALIC, children)
        self.allowed_children = [
            OutputFormatType.TEXT,
            OutputFormatType.BOLD,
            OutputFormatType.LINK,
            OutputFormatType.DOLLAR_OBJECT,
        ]


class OutputFormatCode(OutputFormatText):

    def __init__(self, text):
        super().__init__(text)
        self.format_type = OutputFormatType.CODE


class OutputFormatLink(OutputFormat):

    def __init__(self, href: str, children: List[OutputFormat]):
        super().__init__(OutputFormatType.LINK, children)
        self.href = href
        self.allowed_children = [
            OutputFormatType.TEXT,
            OutputFormatType.BOLD,
            OutputFormatType.ITALIC
        ]

    def get_href(self):
        return self.href


class OutputFormatHeader(OutputFormatBlock):

    def __init__(self, level: int, children: List[OutputFormat]):
        super().__init__(OutputFormatType.HEADER, children)
        self.level = level
        self.allowed_children = [
            OutputFormatType.TEXT,
            OutputFormatType.BOLD,
            OutputFormatType.ITALIC,
            OutputFormatType.LINK,
            OutputFormatType.DOLLAR_OBJECT,
            OutputFormatType.CODE,
        ]

    def get_level(self):
        return self.level


class OutputFormatParagraph(OutputFormatBlock):

    def __init__(self, children: List[OutputFormat]):
        super().__init__(OutputFormatType.PARAGRAPH, children)
        self.allowed_children = [
            OutputFormatType.TEXT,
            OutputFormatType.BOLD,
            OutputFormatType.ITALIC,
            OutputFormatType.LINK,
            OutputFormatType.DOLLAR_OBJECT,
            OutputFormatType.CODE,
        ]


class OutputFormatOrderedList(OutputFormatBlock):

    def __init__(self, children: List[OutputFormat]):
        super().__init__(OutputFormatType.ORDERED_LIST, children)
        self.allowed_children = [
            OutputFormatType.LIST_ITEM,
            OutputFormatType.ORDERED_LIST,
            OutputFormatType.UNORDERED_LIST,
        ]


class OutputFormatUnorderedList(OutputFormatBlock):

    def __init__(self, children: List[OutputFormat]):
        super().__init__(OutputFormatType.UNORDERED_LIST, children)
        self.allowed_children = [
            OutputFormatType.LIST_ITEM,
            OutputFormatType.ORDERED_LIST,
            OutputFormatType.UNORDERED_LIST,
        ]


class OutputFormatListItem(OutputFormatBlock):

    def __init__(self, children: List[OutputFormat]):
        super().__init__(OutputFormatType.LIST_ITEM, children)
        self.allowed_children = [
            OutputFormatType.TEXT,
            OutputFormatType.BOLD,
            OutputFormatType.ITALIC,
            OutputFormatType.LINK,
            OutputFormatType.DOLLAR_OBJECT,
            OutputFormatType.CODE,
        ]


class OutputFormatCodeBlock(OutputFormatBlock):

    def __init__(self, code_type, text):
        super().__init__(OutputFormatType.CODE_BLOCK, [])
        self.code_type = code_type
        self.text = text

    def get_code_type(self):
        return self.code_type

    def get_text(self):
        return self.text


class OutputFormatQuoteBlock(OutputFormatBlock):

    def __init__(self, children: List[OutputFormat]):
        super().__init__(OutputFormatType.QUOTE_BLOCK, children)
        self.allowed_children = [
            OutputFormatType.HEADER,
            OutputFormatType.PARAGRAPH,
            OutputFormatType.ORDERED_LIST,
            OutputFormatType.UNORDERED_LIST,
            OutputFormatType.CODE_BLOCK,
            OutputFormatType.QUOTE_BLOCK,
        ]


class OutputFormatDefinition(OutputFormatBlock):

    def __init__(self, defined_children: List[OutputFormat], definition_children: List[OutputFormat]):
        super().__init__(OutputFormatType.DEFINITION, [])
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

    def get_defined_children(self):
        return self.defined_children

    def get_definition_children(self):
        return self.definition_children

    def validate(self):
        for child in self.defined_children:
            if child.get_format_type() not in self.allowed_children:
                raise DollarException(
                    "{} is not allowed in {}".format(child.get_format_type(), self.get_format_type()))
        for child in self.definition_children:
            if child.get_format_type() not in self.allowed_children:
                raise DollarException(
                    "{} is not allowed in {}".format(child.get_format_type(), self.get_format_type()))


class OutputFormatPluginBlock(OutputFormatBlock):

    def __init__(self, plugin_name, text):
        super().__init__(OutputFormatType.PLUGIN_BLOCK, [])
        self.plugin_name = plugin_name
        self.text = text

    def get_plugin_name(self):
        return self.plugin_name

    def get_text(self):
        return self.text


class OutputFormatDollarObject(OutputFormat):

    def __init__(self, dollar_object: DollarObject):
        super().__init__(OutputFormatType.DOLLAR_OBJECT, [])
        self.dollar_object = dollar_object

    def get_dollar_object(self) -> DollarObject:
        return self.dollar_object

    def get_href(self, this_dollar_object) -> str:
        fr = this_dollar_object.get_target_path().split("/")
        to = self.dollar_object.get_target_path().split("/")
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
