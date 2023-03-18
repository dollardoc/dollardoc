from typing import List

from dollar.dollarexecutionexception import DollarExecutionException
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
from dollar.format.raw.rawdollarformattype import RawDollarFormatType
from dollar.helper.dollarobjecthelper import DollarObjectHelper
from dollar.plugin.pluginmap import PluginMap


class _DollarReferenceObject:

    def __init__(self, dollar_object: DollarObject, value = None):
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
    def transform(cls, this_dollar_object: DollarObject, raw_format: RawDollarFormat):
            if raw_format.getformattype() == RawDollarFormatType.TEXT:
                return InputFormatText(raw_format.gettext())
            elif raw_format.getformattype() == RawDollarFormatType.REFERENCE:
                dollar_reference_object = cls._handledollarparse(this_dollar_object, raw_format.gettargettext())
                if dollar_reference_object.hasvalue():
                    return InputFormatDollarObjectValue(
                            dollar_reference_object.getdollarobject(),
                            dollar_reference_object.getvalue())
                else:
                    dollar_reference_object.getdollarobject().addbacklink(this_dollar_object)
                    return InputFormatDollarObject(dollar_reference_object.getdollarobject())
            elif raw_format.getformattype() == RawDollarFormatType.FUNCTION:
                plugin = PluginMap.getfunction(raw_format.getfunctionname())
                transformed_params = cls.transform_list(this_dollar_object, raw_format.getparameters())
                params = []
                for transformed_param in transformed_params:
                    if transformed_param.getformattype() == InputFormatType.TEXT:
                        params.append(transformed_param.gettext().strip())
                    elif transformed_param.getformattype() == InputFormatType.DOLLAR_OBJECT:
                        params.append(transformed_param.getdollarobject())
                    elif transformed_param.getformattype() == InputFormatType.DOLLAR_OBJECT_VALUE:
                        params.append(transformed_param.getvalue())
                    elif transformed_param.getformattype() == InputFormatType.UNION:
                        param_result = ""
                        for child in transformed_param.getchildren():
                            if child.getformattype() == InputFormatType.TEXT:
                                param_result = param_result + child.gettext()
                            elif child.getformattype() == InputFormatType.DOLLAR_OBJECT:
                                child_dollar_object = child.getdollarobject()
                                child_title = DollarObjectHelper.gettitle(child_dollar_object)
                                param_result = param_result + child_title
                            elif child.getformattype() == InputFormatType.DOLLAR_OBJECT_VALUE:
                                if type(child.getvalue()) == str:
                                    param_result = param_result + child.getvalue()
                                else:
                                    raise DollarExecutionException(
                                            "Type of value needs to be str when rendering Union parameter value, was {}"
                                                    .format(type(child.getvalue())))
                            else:
                                raise DollarExecutionException(
                                        "Format type {} is not supported when rendering Union parameter"
                                                .format(child.getformattype()))
                        params.append(param_result.strip())
                    else:
                        raise DollarExecutionException(
                                "Format type {} is not supported when rendering parameter"
                                        .format(transformed_param.getformattype()))
                return InputFormatFunction(plugin, params, this_dollar_object)
            elif raw_format.getformattype() == RawDollarFormatType.BLOCK:
                plugin = PluginMap.getblock(raw_format.getblockname())
                content = cls.transform(this_dollar_object, raw_format.getcontent())
                return InputFormatBlock(plugin, content)
            elif raw_format.getformattype() == RawDollarFormatType.UNION:
                children = cls.transform_list(this_dollar_object, raw_format.getchildren())
                return InputFormatUnion(children)
            else:
                raise DollarExecutionException("Format {} is not supported".format(raw_format.getformattype()))

    @classmethod
    def transform_list(cls, this_dollar_object: DollarObject, raw_formats: List[RawDollarFormat]):
        result = []
        for raw_format in raw_formats:
            result.append(cls.transform(this_dollar_object, raw_format))
        return result

    @classmethod
    def _handledollarparse(cls, this_dollar_object: DollarObject, dollar_str: str) -> _DollarReferenceObject:
        dollar_str_split = dollar_str.split(".")
        id = dollar_str_split[0]
        if id == "this":
            dollar_object = this_dollar_object
        else:
            dollar_object = DollarObjectIdMap.get(id)
        check = dollar_object.getheader()
        value = None
        for i in range(1, len(dollar_str_split)):
            key = dollar_str_split[i]
            if key not in check:
                raise DollarExecutionException("Key {} could not be found in {}".format(".".join(dollar_str_split[1:]), id))
            value = check[key]
            check = value
        return _DollarReferenceObject(dollar_object, value)
