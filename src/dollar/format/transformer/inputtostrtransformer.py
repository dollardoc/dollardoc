from typing import List
from typing import cast

from dollar.dollarexception import DollarExecutionException
from dollar.dollarexception import DollarException
from dollar.dollarobject import DollarObject
from dollar.helper.validationhelper import ValidationHelper
from dollar.format.input.inputformat import InputFormat
from dollar.format.input.inputformat import InputFormatText
from dollar.format.input.inputformat import InputFormatDollarObject
from dollar.format.input.inputformat import InputFormatDollarObjectValue
from dollar.format.input.inputformat import InputFormatFunction
from dollar.format.input.inputformat import InputFormatBlock
from dollar.format.input.inputformat import InputFormatUnion
from dollar.format.input.inputformattype import InputFormatType
from dollar.format.output.outputfactory import OutputFactory
from dollar.format.output.outputformatter import OutputFormatter
from dollar.plugin.pluginargvalidatior import PluginArgValidator
from dollar.plugin.pluginmap import PluginMap


class InputToStrTransformer:

    @classmethod
    def transform(
            cls,
            output_formatter: OutputFormatter,
            this_dollar_object: DollarObject,
            input_format: InputFormat,
            plugin_map: PluginMap) -> str:
        if input_format.get_format_type() == InputFormatType.TEXT:
            input_format = cast(InputFormatText, input_format)
            return input_format.get_text()

        elif input_format.get_format_type() == InputFormatType.DOLLAR_OBJECT:
            input_format = cast(InputFormatDollarObject, input_format)
            return OutputFactory.create_link_dollar_object(
                    output_formatter,
                    this_dollar_object,
                    input_format.get_dollar_object())

        elif input_format.get_format_type() == InputFormatType.DOLLAR_OBJECT_VALUE:
            input_format = cast(InputFormatDollarObjectValue, input_format)
            if type(input_format.get_value()) == str:
                if not ValidationHelper.valid_str(input_format.get_value()):
                    raise DollarExecutionException(
                            "When rendering, dollar header referenced value needs to be a non blank str",
                            input_format.get_dollar_context())
                return input_format.get_value()
            elif isinstance(input_format.get_value(), DollarObject):
                return OutputFactory.create_link_dollar_object(
                        output_formatter,
                        this_dollar_object,
                        input_format.get_value())
            else:
                raise DollarExecutionException(
                        "When rendering, dollar header referenced value needs to be str or DollarObject",
                        input_format.get_dollar_context())

        elif input_format.get_format_type() == InputFormatType.FUNCTION:
            input_format = cast(InputFormatFunction, input_format)
            plugin = input_format.get_function_plugin()
            params = input_format.get_parameters()
            plugin.get_arg_info()

            try:
                PluginArgValidator.validate(params, plugin.get_arg_info(), plugin_map)
                plugin_output = plugin.exec_function(*params)
                return output_formatter.format(this_dollar_object, plugin_output)
            except DollarException as e:
                raise DollarExecutionException(
                        e.get_message(),
                        input_format.get_dollar_context()) from e

        elif input_format.get_format_type() == InputFormatType.BLOCK:
            input_format = cast(InputFormatBlock, input_format)
            plugin = input_format.get_block_plugin()
            content = input_format.get_content()
            plugin_output = plugin.exec_block(content)
            try:
                return output_formatter.format(this_dollar_object, plugin_output)
            except DollarException as e:
                raise DollarExecutionException(
                        e.get_message(),
                        input_format.get_dollar_context()) from e

        elif input_format.get_format_type() == InputFormatType.UNION:
            input_format = cast(InputFormatUnion, input_format)
            return cls.transform_list(output_formatter, this_dollar_object, input_format.get_children(), plugin_map)

        else:
            raise DollarExecutionException(
                    "Format {} is not supported".format(input_format.get_format_type()),
                    input_format.get_dollar_context())

    @classmethod
    def transform_list(
            cls,
            output_formatter: OutputFormatter,
            this_dollar_object: DollarObject,
            input_formats: List[InputFormat],
            plugin_map: PluginMap):
        result = []
        for input_format in input_formats:
            result.append(cls.transform(output_formatter, this_dollar_object, input_format, plugin_map))
        return "".join(result)
