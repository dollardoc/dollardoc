from dollar.plugin.dollarplugin import DollarFunctionPlugin
from dollar.dollarobject import DollarObject
from dollar.format.output.outputformat import OutputFormatText
from dollar.format.output.outputformat import OutputFormatDefinition
from dollar.format.output.outputformat import OutputFormatDollarObject


class LinkFunctionPlugin(DollarFunctionPlugin):

    def getname(self):
        return "Link"

    def execfunction(self, dollar_object: DollarObject):
        return [
            OutputFormatDefinition([
                OutputFormatDollarObject(dollar_object)
            ], [
                OutputFormatText(dollar_object.getheader()['description'])
            ])
        ]
