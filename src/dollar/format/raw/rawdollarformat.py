from typing import List

from dollar.dollarexception import DollarExecutionException
from dollar.dollarcontext import DollarContext
from dollar.helper.validationhelper import ValidationHelper
from dollar.format.raw.rawdollarformattype import RawDollarFormatType


class RawDollarFormat:

    def __init__(self, format_type: RawDollarFormatType, dollar_context: DollarContext):
        self.format_type = format_type
        self.dollar_context = dollar_context

    def get_format_type(self) -> RawDollarFormatType:
        return self.format_type

    def validate(self):
        pass

    def get_dollar_context(self) -> DollarContext:
        return self.dollar_context

    def __repr__(self):
        return str(self.__dict__)


class RawDollarFormatText(RawDollarFormat):

    def __init__(self, text: str, dollar_context: DollarContext):
        super().__init__(RawDollarFormatType.TEXT, dollar_context)
        self.text = text

    def get_text(self) -> str:
        return self.text

    def validate(self):
        if ValidationHelper.valid_str(self.text):
            raise DollarExecutionException("Text can not be blank")


class RawDollarFormatReference(RawDollarFormat):

    def __init__(self, target_text: str, dollar_context: DollarContext):
        super().__init__(RawDollarFormatType.REFERENCE, dollar_context)
        self.target_text = target_text

    def get_target_text(self) -> str:
        return self.target_text

    def validate(self):
        if ValidationHelper.valid_str(self.target_text):
            raise DollarExecutionException("Target text can not be blank")


class RawDollarFormatFunction(RawDollarFormat):

    def __init__(self, function_name: str, parameters: List[RawDollarFormat], dollar_context: DollarContext):
        super().__init__(RawDollarFormatType.FUNCTION, dollar_context)
        self.function_name = function_name
        self.parameters = parameters

    def get_function_name(self) -> str:
        return self.function_name

    def get_parameters(self) -> List[RawDollarFormat]:
        return self.parameters

    def validate(self):
        if ValidationHelper.valid_str(self.function_name):
            raise DollarExecutionException("Function name can not be blank")
        for param in self.parameters:
            param.validate()


class RawDollarFormatBlock(RawDollarFormat):

    def __init__(self, block_name: str, content: RawDollarFormat, dollar_context: DollarContext):
        super().__init__(RawDollarFormatType.BLOCK, dollar_context)
        self.block_name = block_name
        self.content = content

    def get_block_name(self) -> str:
        return self.block_name

    def get_content(self) -> RawDollarFormat:
        return self.content

    def validate(self):
        if ValidationHelper.valid_str(self.block_name):
            raise DollarExecutionException("Block name can not be blank")
        self.content.validate()


class RawDollarFormatUnion(RawDollarFormat):

    def __init__(self, children: List[RawDollarFormat], dollar_context: DollarContext):
        super().__init__(RawDollarFormatType.UNION, dollar_context)
        self.children = children

    def get_children(self) -> List[RawDollarFormat]:
        return self.children

    def validate(self):
        for child in self.children:
            if child.get_format_type() == RawDollarFormatType.UNION:
                raise DollarExecutionException("A union cant contain another union")
            child.validate()
