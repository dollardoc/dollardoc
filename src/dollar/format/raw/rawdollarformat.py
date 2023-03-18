from typing import List

from dollar.dollarexecutionexception import DollarExecutionException
from dollar.validationhelper import ValidationHelper
from dollar.format.raw.rawdollarformattype import RawDollarFormatType


class RawDollarFormat:

    def __init__(self, format_type: RawDollarFormatType):
        self.format_type = format_type

    def getformattype(self) -> RawDollarFormatType:
        return self.format_type

    def validate(self):
        pass

    def __repr__(self):
        return str(self.__dict__)


class RawDollarFormatText(RawDollarFormat):

    def __init__(self, text: str):
        self.format_type = RawDollarFormatType.TEXT
        self.text = text

    def gettext(self) -> str:
        return self.text

    def validate(self):
        if ValidationHelper.validstr(self.text):
            raise DollarExecutionException("Text can not be blank")


class RawDollarFormatReference(RawDollarFormat):

    def __init__(self, target_text: str):
        self.format_type = RawDollarFormatType.REFERENCE
        self.target_text = target_text

    def gettargettext(self) -> str:
        return self.target_text

    def validate(self):
        if ValidationHelper.validstr(self.target_text):
            raise DollarExecutionException("Target text can not be blank")


class RawDollarFormatFunction(RawDollarFormat):

    def __init__(self, function_name: str, parameters: List[RawDollarFormat]):
        self.format_type = RawDollarFormatType.FUNCTION
        self.function_name = function_name
        self.parameters = parameters

    def getfunctionname(self) -> str:
        return self.function_name

    def getparameters(self) -> List[RawDollarFormat]:
        return self.parameters

    def validate(self):
        if ValidationHelper.validstr(self.function_name):
            raise DollarExecutionException("Function name can not be blank")
        for param in self.parameters:
            param.validate()


class RawDollarFormatBlock(RawDollarFormat):

    def __init__(self, block_name: str, content: RawDollarFormat):
        self.format_type = RawDollarFormatType.BLOCK
        self.block_name = block_name
        self.content = content

    def getblockname(self) -> str:
        return self.block_name

    def getcontent(self) -> RawDollarFormat:
        return self.content

    def validate(self):
        if ValidationHelper.validstr(self.block_name):
            raise DollarExecutionException("Block name can not be blank")
        self.content.validate()


class RawDollarFormatUnion(RawDollarFormat):

    def __init__(self, children: List[RawDollarFormat]):
        self.format_type = RawDollarFormatType.UNION
        self.children = children

    def getchildren(self) -> List[RawDollarFormat]:
        return self.children

    def validate(self):
        for child in self.children:
            if child.getformattype() == RawDollarFormatType.UNION:
                raise DollarExecutionException("A union cant contain another union")
            child.validate()
