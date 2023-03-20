from typing import List

from dollar.plugin.dollarplugin import DollarFunctionPlugin
from dollar.dollarobject import DollarObject
from dollar.format.output.outputformat import OutputFormatText
from dollar.format.output.outputformat import OutputFormatUnorderedList
from dollar.format.output.outputformat import OutputFormatListItem
from dollar.format.output.outputformat import OutputFormatDollarObject
from dollar.plugin.pluginarg import PluginArg


class ListFunctionPlugin(DollarFunctionPlugin):

    def get_name(self):
        return "List"

    def get_arg_info(self) -> List[PluginArg]:
        return [
            PluginArg(
                    "input_list",
                    List,
                    "List which will be printed"),
        ]

    def exec_function(self, input_list):
        output_items = []
        for item in input_list:
            if isinstance(item, DollarObject):
                output_items.append(
                        OutputFormatListItem([
                            OutputFormatDollarObject(item)
                        ]))
            elif type(item) == str:
                output_items.append(
                        OutputFormatListItem([
                            OutputFormatText(item)
                        ]))
        return [OutputFormatUnorderedList(output_items)]
