from typing import List

from dollar.plugin.dollarplugin import DollarFunctionPlugin
from dollar.dollarobject import DollarObject
from dollar.format.output.outputformat import OutputFormatUnorderedList
from dollar.format.output.outputformat import OutputFormatListItem
from dollar.format.output.outputformat import OutputFormatDollarObject
from dollar.plugin.pluginarg import PluginArg
from dollar.plugin.pluginarg import PluginArgDollarObject


class ListBackLinksFunctionPlugin(DollarFunctionPlugin):

    def get_name(self):
        return "ListBackLinks"

    def get_arg_info(self) -> List[PluginArg]:
        return [
            PluginArgDollarObject(
                    None,
                    "Dollar object of which to list backlinks"),
        ]

    def exec_function(self, dollar_object: DollarObject):
        output = []
        for ref in dollar_object.get_backlinks():
            output.append(OutputFormatListItem([
                OutputFormatDollarObject(ref)
            ]))
        return [
            OutputFormatUnorderedList(output)
        ]
