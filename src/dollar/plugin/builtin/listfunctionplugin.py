from dollar.plugin.dollarplugin import DollarFunctionPlugin
from dollar.dollarobject import DollarObject
from dollar.format.output.outputformat import OutputFormatText
from dollar.format.output.outputformat import OutputFormatUnorderedList
from dollar.format.output.outputformat import OutputFormatListItem
from dollar.format.output.outputformat import OutputFormatDollarObject


class ListFunctionPlugin(DollarFunctionPlugin):

    def getname(self):
        return "List"

    def execfunction(self, input_list):
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
        return [ OutputFormatUnorderedList(output_items) ]
#            dollar.OutputFormatQuoteBlock([
#                dollar.OutputFormatHeader(1, [
#                    dollar.OutputFormatText("TEST1")
#                ]),
#                dollar.OutputFormatQuoteBlock([
#                    dollar.OutputFormatHeader(2, [
#                        dollar.OutputFormatText("TEST2")
#                    ]),
#                    dollar.OutputFormatParagraph([
#                        dollar.OutputFormatText("TEST3")
#                    ]),
#                    dollar.OutputFormatQuoteBlock([
#                        dollar.OutputFormatHeader(4, [
#                            dollar.OutputFormatText("TEST SUB")
#                        ]),
#                        dollar.OutputFormatParagraph([
#                            dollar.OutputFormatText("TEST SUB 2")
 #                       ]),
 #                   ]),
 #                   dollar.OutputFormatParagraph([
 #                       dollar.OutputFormatText("TEST3")
 #                   ]),
 #                   dollar.OutputFormatCodeBlock("TESTCODE", "public\nstatic\ntest")
 #               ])
 #           ]),
 #           dollar.OutputFormatDefinition([
 #               dollar.OutputFormatDollarObject(input_list[0])
 #           ], [
 #               dollar.OutputFormatText("THIS MEANS Y")
 #           ])
