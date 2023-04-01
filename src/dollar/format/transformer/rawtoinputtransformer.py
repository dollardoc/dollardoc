from typing import List
from typing import cast

from dollar.dollarexception import DollarExecutionException
from dollar.dollarexception import DollarException
from dollar.dollarcontext import DollarContext
from dollar.dollarobject import DollarObject
from dollar.dollarobjectidmap import DollarObjectIdMap
from dollar.format.input.inputformat import InputFormatText
from dollar.format.input.inputformat import InputFormatDollarObject
from dollar.format.input.inputformat import InputFormatDollarObjectValue
from dollar.format.input.inputformat import InputFormatFunction
from dollar.format.input.inputformat import InputFormatBlock
from dollar.format.input.inputformat import InputFormatUnion
from dollar.format.input.inputformattype import InputFormatType
from dollar.format.raw.rawdollarformat import RawDollarFormat
from dollar.format.raw.rawdollarformat import RawDollarFormatText
from dollar.format.raw.rawdollarformat import RawDollarFormatReference
from dollar.format.raw.rawdollarformat import RawDollarFormatFunction
from dollar.format.raw.rawdollarformat import RawDollarFormatBlock
from dollar.format.raw.rawdollarformat import RawDollarFormatUnion
from dollar.format.raw.rawdollarformattype import RawDollarFormatType
from dollar.helper.dollarobjecthelper import DollarObjectHelper
from dollar.plugin.pluginmap import PluginMap


class _DollarReferenceObject:

    def __init__(self, dollar_object: DollarObject, value=None):
        self.dollar_object = dollar_object
        self.value = value

    def getdollarobject(self) -> DollarObject:
        return self.dollar_object

    def getvalue(self):
        return self.value

    def hasvalue(self):
        return self.value is not None


class RawToInputTransformer:

    @classmethod
    def transform(
            cls,
            this_dollar_object: DollarObject,
            raw_format: RawDollarFormat,
            dollar_id_map: DollarObjectIdMap,
            plugin_map: PluginMap):
        if raw_format.get_format_type() == RawDollarFormatType.TEXT:
            raw_format = cast(RawDollarFormatText, raw_format)
            return InputFormatText(raw_format.get_text(), raw_format.get_dollar_context())

        elif raw_format.get_format_type() == RawDollarFormatType.REFERENCE:
            raw_format = cast(RawDollarFormatReference, raw_format)
            dollar_reference_object = cls._handle_dollar_parse(
                    this_dollar_object,
                    raw_format.get_target_text(),
                    raw_format.get_dollar_context(),
                    dollar_id_map)
            if dollar_reference_object.hasvalue():
                return InputFormatDollarObjectValue(
                        dollar_reference_object.getdollarobject(),
                        dollar_reference_object.getvalue(),
                        raw_format.get_dollar_context())
            else:
                dollar_reference_object.getdollarobject().add_backlink(this_dollar_object)
                return InputFormatDollarObject(
                        dollar_reference_object.getdollarobject(),
                        raw_format.get_dollar_context())

        elif raw_format.get_format_type() == RawDollarFormatType.FUNCTION:
            raw_format = cast(RawDollarFormatFunction, raw_format)
            try:
                plugin = plugin_map.get_function(raw_format.get_function_name())
            except DollarException as e:
                raise DollarExecutionException(e.get_message(), raw_format.get_dollar_context())
            transformed_params = cls.transform_list(this_dollar_object, raw_format.get_parameters(), dollar_id_map, plugin_map)
            params = []
            for transformed_param in transformed_params:
                if transformed_param.get_format_type() == InputFormatType.TEXT:
                    transformed_param = cast(InputFormatText, transformed_param)
                    params.append(transformed_param.get_text().strip())
                elif transformed_param.get_format_type() == InputFormatType.DOLLAR_OBJECT:
                    transformed_param = cast(InputFormatDollarObject, transformed_param)
                    params.append(transformed_param.get_dollar_object())
                elif transformed_param.get_format_type() == InputFormatType.DOLLAR_OBJECT_VALUE:
                    transformed_param = cast(InputFormatDollarObjectValue, transformed_param)
                    params.append(transformed_param.get_value())
                elif transformed_param.get_format_type() == InputFormatType.UNION:
                    transformed_param = cast(InputFormatUnion, transformed_param)
                    param_result = ""
                    for child in transformed_param.get_children():
                        if child.get_format_type() == InputFormatType.TEXT:
                            child = cast(InputFormatText, child)
                            param_result = param_result + child.get_text()
                        elif child.get_format_type() == InputFormatType.DOLLAR_OBJECT:
                            child = cast(InputFormatDollarObject, child)
                            child_dollar_object = child.get_dollar_object()
                            child_title = DollarObjectHelper.get_title(child_dollar_object)
                            param_result = param_result + child_title
                        elif child.get_format_type() == InputFormatType.DOLLAR_OBJECT_VALUE:
                            child = cast(InputFormatDollarObjectValue, child)
                            if type(child.get_value()) == str:
                                param_result = param_result + child.get_value()
                            else:
                                raise DollarExecutionException(
                                        "Type of value needs to be str when rendering Union parameter value, was {}"
                                        .format(type(child.get_value())),
                                        child.get_dollar_context())
                        else:
                            raise DollarExecutionException(
                                    "Format type {} is not supported when rendering Union parameter"
                                    .format(child.get_format_type()),
                                    child.get_dollar_context())
                    params.append(param_result.strip())
                else:
                    raise DollarExecutionException(
                            "Format type {} is not supported when rendering parameter"
                            .format(transformed_param.get_format_type()),
                            transformed_param.get_dollar_context())
            return InputFormatFunction(plugin, params, this_dollar_object, raw_format.get_dollar_context())

        elif raw_format.get_format_type() == RawDollarFormatType.BLOCK:
            raw_format = cast(RawDollarFormatBlock, raw_format)
            try:
                plugin = plugin_map.get_block(raw_format.get_block_name())
            except DollarException as e:
                raise DollarExecutionException(e.get_message(), raw_format.get_dollar_context())
            content = cls.transform(this_dollar_object, raw_format.get_content(), dollar_id_map, plugin_map)
            return InputFormatBlock(plugin, content, raw_format.get_dollar_context())

        elif raw_format.get_format_type() == RawDollarFormatType.UNION:
            raw_format = cast(RawDollarFormatUnion, raw_format)
            children = cls.transform_list(this_dollar_object, raw_format.get_children(), dollar_id_map, plugin_map)
            return InputFormatUnion(children, raw_format.get_dollar_context())

        else:
            raise DollarExecutionException(
                    "Format {} is not supported".format(raw_format.get_format_type()),
                    raw_format.get_dollar_context())

    @classmethod
    def transform_list(
            cls,
            this_dollar_object: DollarObject,
            raw_formats: List[RawDollarFormat],
            dollar_id_map: DollarObjectIdMap,
            plugin_map: PluginMap):
        result = []
        for raw_format in raw_formats:
            result.append(cls.transform(this_dollar_object, raw_format, dollar_id_map, plugin_map))
        return result

    @classmethod
    def _handle_dollar_parse(
            cls,
            this_dollar_object: DollarObject,
            dollar_str: str,
            dollar_context: DollarContext,
            dollar_id_map: DollarObjectIdMap) -> _DollarReferenceObject:
        dollar_str_split = dollar_str.split(".")
        dollar_id = dollar_str_split[0]
        if dollar_id == "this":
            dollar_object = this_dollar_object
        else:
            try:
                dollar_object = dollar_id_map.get(dollar_id)
            except DollarException as e:
                raise DollarExecutionException(e.get_message(), dollar_context) from e
        check = dollar_object.get_header()
        value = None
        for i in range(1, len(dollar_str_split)):
            key = dollar_str_split[i]
            if key not in check:
                raise DollarExecutionException(
                        "Key {} could not be found in {}"
                        .format(".".join(dollar_str_split[1:]), dollar_id),
                        dollar_context)
            value = check[key]
            check = value
        return _DollarReferenceObject(dollar_object, value)
