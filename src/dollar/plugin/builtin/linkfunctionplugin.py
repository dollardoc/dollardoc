from typing import List

from dollar.plugin.dollarplugin import DollarFunctionPlugin
from dollar.dollarobject import DollarObject
from dollar.format.output.outputformat import OutputFormatText
from dollar.format.output.outputformat import OutputFormatDefinition
from dollar.format.output.outputformat import OutputFormatDollarObject
from dollar.plugin.pluginarg import PluginArg
from dollar.plugin.pluginarg import PluginArgDollarObject


class LinkFunctionPlugin(DollarFunctionPlugin):

    def get_name(self):
        return "Link"

    def get_arg_info(self) -> List[PluginArg]:
        return [
            PluginArgDollarObject(
                    "page",
                    "Dollar object of which to create explicit link to"),
        ]

    def exec_function(self, dollar_object: DollarObject):
        return [
            OutputFormatDefinition([
                OutputFormatDollarObject(dollar_object)
            ], [
                OutputFormatText(dollar_object.get_header()['description'])
            ])
        ]
