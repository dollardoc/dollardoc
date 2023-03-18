from typing import List

from dollar.dollarexecutionexception import DollarExecutionException
from dollar.dollarobject import DollarObject
from dollar.validationhelper import ValidationHelper
from dollar.format.input.inputformattype import InputFormatType
from dollar.plugin.dollarplugin import DollarFunctionPlugin
from dollar.plugin.dollarplugin import DollarBlockPlugin


class _InputFormat:

    def __init__(self, format_type: InputFormatType):
        self.format_type = format_type

    def getformattype(self) -> InputFormatType:
        return self.format_type

    def validate(self):
        pass

    def __repr__(self):
        return str(self.__dict__)

class InputFormatText(_InputFormat):

    def __init__(self, text: str):
        self.format_type = InputFormatType.TEXT
        self.text = text

    def gettext(self) -> str:
        return self.text

    def validate(self):
        if ValidationHelper.validstr(self.text):
            raise DollarExecutionException("Text can not be blank")


class InputFormatDollarObject(_InputFormat):

    def __init__(self, dollar_object: DollarObject):
        self.format_type = InputFormatType.DOLLAR_OBJECT
        self.dollar_object = dollar_object

    def getdollarobject(self) -> DollarObject:
        return self.dollar_object

    def validate(self):
        if not isinstance(self.dollar_object, DollarObject):
            raise DollarExecutionException("Dollar object is of wrong type")


class InputFormatDollarObjectValue(InputFormatDollarObject):

    def __init__(self, dollar_object: DollarObject, value):
        self.format_type = InputFormatType.DOLLAR_OBJECT_VALUE
        self.dollar_object = dollar_object
        self.value = value

    def getvalue(self):
        return self.value


class InputFormatFunction(_InputFormat):

    def __init__(self, function_plugin: DollarFunctionPlugin, parameters: List[_InputFormat], from_dollar_object: DollarObject):
        self.format_type = InputFormatType.FUNCTION
        self.function_plugin = function_plugin
        self.parameters = parameters
        self.from_dollar_object = from_dollar_object

    def getfunctionplugin(self) -> DollarFunctionPlugin:
        return self.function_plugin

    def getparameters(self) -> List[_InputFormat]:
        return self.parameters

    def getfromdollarobject(self) -> DollarObject:
        return self.from_dollar_object

    def validate(self):
        if not isinstance(self.function_plugin, DollarFunctionPlugin):
            raise DollarExecutionException("Function plugin is of wrong type")
        for param in self.parameters:
            param.validate()


class InputFormatBlock(_InputFormat):

    def __init__(self, block_plugin: DollarBlockPlugin, content: _InputFormat):
        self.format_type = InputFormatType.BLOCK
        self.block_plugin = block_plugin
        self.content = content

    def getblockplugin(self) -> DollarBlockPlugin:
        return self.block_plugin

    def getcontent(self) -> _InputFormat:
        return self.content

    def validate(self):
        if not isinstance(self.block_plugin, DollarBlockPlugin):
            raise DollarExecutionException("Block plugin is of wrong type")
        self.content.validate()



class InputFormatUnion(_InputFormat):

    def __init__(self, children: List[_InputFormat]):
        self.format_type = InputFormatType.UNION
        self.children = children

    def getchildren(self) -> List[_InputFormat]:
        return self.children

    def validate(self):
        for child in self.children:
            if child.getformattype() == InputFormatType.UNION:
                raise DollarExecutionException("A union cant contain another union")
            child.validate()
