from dollar.plugin.dollarplugin import DollarFunctionPlugin
from dollar.dollarobject import DollarObject
from dollar.format.output.outputformat import OutputFormatUnorderedList
from dollar.format.output.outputformat import OutputFormatListItem
from dollar.format.output.outputformat import OutputFormatDollarObject


class ListBackLinksFunctionPlugin(DollarFunctionPlugin):

    def getname(self):
        return "ListBackLinks"

    def execfunction(self, dollar_object: DollarObject):
        output = []
        for ref in dollar_object.getbacklinks():
            output.append(OutputFormatListItem([
                OutputFormatDollarObject(ref)
            ]))
        return [
            OutputFormatUnorderedList(output)
        ]
