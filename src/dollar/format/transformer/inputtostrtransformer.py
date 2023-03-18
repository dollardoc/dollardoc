from typing import List

from dollar.dollarexecutionexception import DollarExecutionException
from dollar.dollarobject import DollarObject
from dollar.validationhelper import ValidationHelper
from dollar.format.input.inputformat import _InputFormat
from dollar.format.input.inputformattype import InputFormatType
from dollar.format.output.outputfactory import OutputFactory
from dollar.format.output.outputformatterhandler import OutputFormatterHandler


class InputToStrTransformer:

    @classmethod
    def transform(cls, this_dollar_object: DollarObject, input_format: _InputFormat) -> str:
            if input_format.getformattype() == InputFormatType.TEXT:
                return input_format.gettext()

            elif input_format.getformattype() == InputFormatType.DOLLAR_OBJECT:
                return OutputFactory.createlinkdollarobject(this_dollar_object, input_format.getdollarobject())

            elif input_format.getformattype() == InputFormatType.DOLLAR_OBJECT_VALUE:
                if type(input_format.getvalue()) == str:
                    if not ValidationHelper.validstr(input_format.getvalue()):
                        raise DollarExecutionException(
                                "When rendering, dollar header referenced value needs to be a non blank str")
                    return input_format.getvalue()
                elif isinstance(input_format.getvalue(), DollarObject):
                    return OutputFactory.createlinkdollarobject(this_dollar_object, input_format.getdollarobject())
                else:
                    raise DollarExecutionException(
                            "When rendering, dollar header referenced value needs to be str or DollarObject")

            elif input_format.getformattype() == InputFormatType.FUNCTION:
                plugin = input_format.getfunctionplugin()
                params = input_format.getparameters()
                from_dollar_object = input_format.getfromdollarobject()
                plugin_output = plugin.execfunction(*params)
                return OutputFormatterHandler.getformatter().format(this_dollar_object, plugin_output)

            elif input_format.getformattype() == InputFormatType.BLOCK:
                plugin = input_format.getblockplugin()
                content = input_format.getcontent()
                plugin_output = plugin.execblock(content)
                return OutputFormatterHandler.getformatter().format(this_dollar_object, plugin_output)

            elif input_format.getformattype() == InputFormatType.UNION:
                return cls.transform_list(this_dollar_object, input_format.getchildren())

            else:
                raise DollarExecutionException("Format {} is not supported".format(input_format.getformattype()))

    @classmethod
    def transform_list(cls, this_dollar_object: DollarObject, input_formats: List[_InputFormat]):
        result = []
        for input_format in input_formats:
            result.append(cls.transform(this_dollar_object, input_format))
        return "".join(result)