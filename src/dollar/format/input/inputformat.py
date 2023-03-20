from typing import List

from dollar.dollarexception import DollarExecutionException
from dollar.dollarcontext import DollarContext
from dollar.dollarobject import DollarObject
from dollar.helper.validationhelper import ValidationHelper
from dollar.format.input.inputformattype import InputFormatType
from dollar.plugin.dollarplugin import DollarFunctionPlugin
from dollar.plugin.dollarplugin import DollarBlockPlugin


class InputFormat:

    def __init__(self, format_type: InputFormatType, dollar_context: DollarContext):
        self.format_type = format_type
        self.dollar_context = dollar_context

    def get_format_type(self) -> InputFormatType:
        return self.format_type

    def validate(self):
        pass

    def get_dollar_context(self):
        return self.dollar_context

    def __repr__(self):
        return str(self.__dict__)


class InputFormatText(InputFormat):

    def __init__(self, text: str, dollar_context: DollarContext):
        super().__init__(InputFormatType.TEXT, dollar_context)
        self.text = text

    def get_text(self) -> str:
        return self.text

    def validate(self):
        if ValidationHelper.valid_str(self.text):
            raise DollarExecutionException("Text can not be blank", self.dollar_context)


class InputFormatDollarObject(InputFormat):

    def __init__(self, dollar_object: DollarObject, dollar_context: DollarContext):
        super().__init__(InputFormatType.DOLLAR_OBJECT, dollar_context)
        self.dollar_object = dollar_object

    def get_dollar_object(self) -> DollarObject:
        return self.dollar_object

    def validate(self):
        if not isinstance(self.dollar_object, DollarObject):
            raise DollarExecutionException("Dollar object is of wrong type", self.dollar_context)


class InputFormatDollarObjectValue(InputFormatDollarObject):

    def __init__(self, dollar_object: DollarObject, value, dollar_context: DollarContext):
        super().__init__(dollar_object, dollar_context)
        self.format_type = InputFormatType.DOLLAR_OBJECT_VALUE
        self.value = value

    def get_value(self):
        return self.value


class InputFormatFunction(InputFormat):

    def __init__(self,
                 function_plugin: DollarFunctionPlugin,
                 parameters: List[InputFormat],
                 from_dollar_object: DollarObject,
                 dollar_context: DollarContext):
        super().__init__(InputFormatType.FUNCTION, dollar_context)
        self.function_plugin = function_plugin
        self.parameters = parameters
        self.from_dollar_object = from_dollar_object

    def get_function_plugin(self) -> DollarFunctionPlugin:
        return self.function_plugin

    def get_parameters(self) -> List[InputFormat]:
        return self.parameters

    def get_from_dollar_object(self) -> DollarObject:
        return self.from_dollar_object

    def validate(self):
        if not isinstance(self.function_plugin, DollarFunctionPlugin):
            raise DollarExecutionException("Function plugin is of wrong type", self.dollar_context)
        for param in self.parameters:
            param.validate()


class InputFormatBlock(InputFormat):

    def __init__(self, block_plugin: DollarBlockPlugin, content: InputFormat, dollar_context: DollarContext):
        super().__init__(InputFormatType.BLOCK, dollar_context)
        self.block_plugin = block_plugin
        self.content = content

    def get_block_plugin(self) -> DollarBlockPlugin:
        return self.block_plugin

    def get_content(self) -> InputFormat:
        return self.content

    def validate(self):
        if not isinstance(self.block_plugin, DollarBlockPlugin):
            raise DollarExecutionException("Block plugin is of wrong type", self.dollar_context)
        self.content.validate()


class InputFormatUnion(InputFormat):

    def __init__(self, children: List[InputFormat], dollar_context: DollarContext):
        super().__init__(InputFormatType.UNION, dollar_context)
        self.children = children

    def get_children(self) -> List[InputFormat]:
        return self.children

    def validate(self):
        for child in self.children:
            if child.get_format_type() == InputFormatType.UNION:
                raise DollarExecutionException("A union cant contain another union", self.dollar_context)
            child.validate()
