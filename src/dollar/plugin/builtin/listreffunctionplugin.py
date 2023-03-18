from dollar.plugin.dollarplugin import DollarFunctionPlugin
from dollar.dollarobject import DollarObject
from dollar.format.output.outputformat import OutputFormatText
from dollar.format.output.outputformat import OutputFormatDefinition
from dollar.format.output.outputformat import OutputFormatDollarObject


class ListRefFunctionPlugin(DollarFunctionPlugin):

    def getname(self):
        return "ListRef"

    def execfunction(self, dollar_object: DollarObject):
        output = []
        for ref in dollar_object.getbackrefs():
            output.append(OutputFormatDefinition([
                OutputFormatDollarObject(ref)
            ], [
                OutputFormatText(ref.getheader()['description'])
            ]))
        return output
