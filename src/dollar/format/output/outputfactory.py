from dollar.dollarobject import DollarObject
from dollar.format.output.outputformat import OutputFormatText
from dollar.format.output.outputformat import OutputFormatLink
from dollar.format.output.outputformat import OutputFormatDollarObject
from dollar.format.output.outputformatterhandler import OutputFormatterHandler


class OutputFactory:

    @classmethod
    def create_link(cls, this_dollar_object: DollarObject, text, href):
        return OutputFormatterHandler.get_formatter().format_inline(this_dollar_object, [
            OutputFormatLink(href, [
                OutputFormatText(text)
            ])
        ])

    @classmethod
    def create_link_dollar_object(cls, this_dollar_object: DollarObject, to_dollar_object: DollarObject):
        return OutputFormatterHandler.get_formatter().format_inline(this_dollar_object, [
            OutputFormatDollarObject(to_dollar_object)
        ])

    @classmethod
    def create_list(cls, list_structure):
        pass

    @classmethod
    def create_header(cls, text, level):
        pass

    @classmethod
    def create_code_block(cls, code_block_type, code):
        pass

    @classmethod
    def create_plugin_block(cls, plugin_block_type, code):
        return cls.create_code_block(plugin_block_type, code)

    @classmethod
    def create_definition(cls, item, definition):
        pass
