from dollar.dollarobject import DollarObject
from dollar.format.output.outputformat import OutputFormatText
from dollar.format.output.outputformat import OutputFormatLink
from dollar.format.output.outputformat import OutputFormatDollarObject
from dollar.format.output.outputformatterhandler import OutputFormatterHandler


class OutputFactory:

    @classmethod
    def createlink(cls, this_dollar_object: DollarObject, text, href):
        return OutputFormatterHandler.getformatter().format_inline(this_dollar_object, [
            OutputFormatLink(href, [
                OutputFormatText(text)
            ])
        ])

    @classmethod
    def createlinkdollarobject(cls, this_dollar_object: DollarObject, to_dollar_object: DollarObject):
        return OutputFormatterHandler.getformatter().format_inline(this_dollar_object, [
            OutputFormatDollarObject(to_dollar_object)
        ])

    @classmethod
    def createlist(cls, list_structure):
        pass

    @classmethod
    def createheader(cls, text, level):
        pass

    @classmethod
    def createcodeblock(cls, type, code):
        pass

    @classmethod
    def createpluginblock(cls, type, code):
        return cls.createcodeblock(type, code)

    @classmethod
    def createdefinition(cls, item, definition):
        pass
