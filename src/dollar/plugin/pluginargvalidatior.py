from typing import List
from typing import cast

from dollar.helper.dollarobjecthelper import DollarObjectHelper
from dollar.plugin.pluginarg import PluginArg
from dollar.plugin.pluginarg import PluginArgDollarObject
from dollar.plugin.pluginmap import PluginMap
from dollar.dollarexception import DollarException
from dollar.dollarobject import DollarObject


class PluginArgValidator:

    @staticmethod
    def validate(args: List, args_info: List[PluginArg], plugin_map: PluginMap):
        if len(args) != len(args_info):
            raise DollarException(
                    "Provided {} argument, {} needed"
                    .format(len(args), len(args_info)))
        for i in range(0, len(args)):
            arg = args[i]
            arg_info = args_info[i]
            if not isinstance(arg, arg_info.get_arg_type()):
                raise DollarException(
                        "Type missmatch of argument #{}, {} is not of type {}"
                        .format(i+1, type(arg), arg_info.get_arg_type()))
            if isinstance(arg_info, PluginArgDollarObject):
                dollar_object = cast(DollarObject, arg)
                arg_info = cast(PluginArgDollarObject, arg_info)
                dollar_object_type = arg_info.get_dollar_object_type()
                if dollar_object_type is not None:
                    if not DollarObjectHelper.is_type(dollar_object, dollar_object_type, plugin_map):
                        raise DollarException(
                                "DollarObject with id {}, was not of expected type {}"
                                .format(dollar_object.get_id(), dollar_object_type))
