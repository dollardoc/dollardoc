from typing import List

from dollar.plugin.dollarplugin import DollarFunctionPlugin
from dollar.dollarobject import DollarObject
from dollar.format.output.outputformat import OutputFormatText
from dollar.format.output.outputformat import OutputFormatDefinition
from dollar.format.output.outputformat import OutputFormatDollarObject
from dollar.plugin.pluginarg import PluginArg
from dollar.plugin.pluginarg import PluginArgDollarObject


class ListRefFunctionPlugin(DollarFunctionPlugin):

    def get_name(self):
        return "ListRef"

    def get_arg_info(self) -> List[PluginArg]:
        return [
            PluginArgDollarObject(
                    "page",
                    "Dollar object of which to list references"),
        ]

    def exec_function(self, dollar_object: DollarObject):
        output = []
        for ref in dollar_object.get_backrefs():
            output.append(OutputFormatDefinition([
                OutputFormatDollarObject(ref)
            ], [
                OutputFormatText(ref.get_header()['description'])
            ]))
        return output
