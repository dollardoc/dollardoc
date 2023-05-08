from dollar.format.output.outputformatter import OutputFormatterMarkdown
from dollar.format.output.outputformatdollarobjectlinktype import OutputFormatDollarObjectLinkType


class OutputFormatterHandler:

    @classmethod
    def get_formatter(cls, output_format_dollar_object_link_type: OutputFormatDollarObjectLinkType) -> OutputFormatterMarkdown:
        return OutputFormatterMarkdown(output_format_dollar_object_link_type)
