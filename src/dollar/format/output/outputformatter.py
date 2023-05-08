from typing import List
from typing import cast

from dollar.dollarexception import DollarExecutionException
from dollar.dollarobject import DollarObject
from dollar.format.output.outputformat import OutputFormat
from dollar.format.output.outputformattype import OutputFormatType
from dollar.format.output.outputformat import OutputFormatText
from dollar.format.output.outputformat import OutputFormatBold
from dollar.format.output.outputformat import OutputFormatItalic
from dollar.format.output.outputformat import OutputFormatCode
from dollar.format.output.outputformat import OutputFormatLink
from dollar.format.output.outputformat import OutputFormatHeader
from dollar.format.output.outputformat import OutputFormatParagraph
from dollar.format.output.outputformat import OutputFormatOrderedList
from dollar.format.output.outputformat import OutputFormatUnorderedList
from dollar.format.output.outputformat import OutputFormatListItem
from dollar.format.output.outputformat import OutputFormatCodeBlock
from dollar.format.output.outputformat import OutputFormatQuoteBlock
from dollar.format.output.outputformat import OutputFormatDefinition
from dollar.format.output.outputformat import OutputFormatPluginBlock
from dollar.format.output.outputformat import OutputFormatDollarObject
from dollar.format.output.outputformatdollarobjectlinktype import OutputFormatDollarObjectLinkType


class OutputFormatter:

    def format(self, this_dollar_object: DollarObject, dollar_formats: List[OutputFormat], context="") -> str:
        pass

    def format_inline(self, this_dollar_object: DollarObject, dollar_formats: List[OutputFormat]) -> str:
        pass


class OutputFormatterMarkdown(OutputFormatter):

    def __init__(self, output_format_dollar_object_link_type: OutputFormatDollarObjectLinkType):
        self.link_type = output_format_dollar_object_link_type

    def format(self, this_dollar_object: DollarObject, dollar_formats: List[OutputFormat], context="") -> str:
        result = []
        for dollar_format in dollar_formats:
            dollar_format.validate()
            dollar_format_type = dollar_format.get_format_type()
            if not dollar_format.is_block():
                raise DollarExecutionException(
                        "{} is not allowed as a root level block".format(dollar_format.get_format_type()))

            if dollar_format_type == OutputFormatType.HEADER:
                dollar_format = cast(OutputFormatHeader, dollar_format)
                head = ""
                for i in range(0, dollar_format.get_level()):
                    head = head + "#"
                result.append(
                        context
                        + head
                        + " "
                        + self.format_inline(this_dollar_object, dollar_format.get_children()))

            elif dollar_format_type == OutputFormatType.PARAGRAPH:
                dollar_format = cast(OutputFormatParagraph, dollar_format)
                result.append(context + self.format_inline(this_dollar_object, dollar_format.get_children()))

            elif dollar_format_type == OutputFormatType.ORDERED_LIST:
                dollar_format = cast(OutputFormatOrderedList, dollar_format)
                result.append(
                        context
                        + self.format_list(this_dollar_object, dollar_format.get_children(), True, context))

            elif dollar_format_type == OutputFormatType.UNORDERED_LIST:
                dollar_format = cast(OutputFormatUnorderedList, dollar_format)
                result.append(
                        context
                        + self.format_list(this_dollar_object, dollar_format.get_children(), False, context))

            elif dollar_format_type == OutputFormatType.CODE_BLOCK:
                dollar_format = cast(OutputFormatCodeBlock, dollar_format)
                join_str = "\n" + context
                text = join_str.join(dollar_format.get_text().split("\n"))
                result.append(
                        context
                        + "``` "
                        + dollar_format.get_code_type()
                        + "\n"
                        + context
                        + text
                        + "\n"
                        + context
                        + "```")

            elif dollar_format_type == OutputFormatType.QUOTE_BLOCK:
                dollar_format = cast(OutputFormatQuoteBlock, dollar_format)
                result.append(self.format(this_dollar_object, dollar_format.get_children(), context + "> "))

            elif dollar_format_type == OutputFormatType.DEFINITION:
                dollar_format = cast(OutputFormatDefinition, dollar_format)
                result.append(
                        context
                        + self.format_inline(this_dollar_object, dollar_format.get_defined_children())
                        + "\n"
                        + context
                        + ": "
                        + self.format_inline(this_dollar_object, dollar_format.get_definition_children()))

            elif dollar_format_type == OutputFormatType.PLUGIN_BLOCK:
                dollar_format = cast(OutputFormatPluginBlock, dollar_format)
                join_str = "\n" + context
                text = join_str.join(dollar_format.get_text().split("\n"))
                result.append(
                        context
                        + "``` "
                        + dollar_format.get_plugin_name()
                        + "\n"
                        + context
                        + text
                        + "\n"
                        + context
                        + "```")

            else:
                raise DollarExecutionException(
                        "{} is not allowed as a root level block".format(dollar_format.get_format_type()))

        join_str = "\n" + context + "\n"
        return join_str.join(result)

    def format_inline(self, this_dollar_object: DollarObject, dollar_formats: List[OutputFormat]) -> str:
        result = ""
        for dollar_format in dollar_formats:
            dollar_format.validate()
            dollar_format_type = dollar_format.get_format_type()
            if dollar_format.is_block():
                raise DollarExecutionException(
                        "{} is not allowed as a nested inline item".format(dollar_format.get_format_type()))

            if dollar_format_type == OutputFormatType.TEXT:
                dollar_format = cast(OutputFormatText, dollar_format)
                result = result + dollar_format.get_text()

            elif dollar_format_type == OutputFormatType.BOLD:
                dollar_format = cast(OutputFormatBold, dollar_format)
                result = result + "**" + self.format_inline(this_dollar_object, dollar_format.get_children()) + "**"

            elif dollar_format_type == OutputFormatType.ITALIC:
                dollar_format = cast(OutputFormatItalic, dollar_format)
                result = result + "*" + self.format_inline(this_dollar_object, dollar_format.get_children()) + "*"

            elif dollar_format_type == OutputFormatType.CODE:
                dollar_format = cast(OutputFormatCode, dollar_format)
                result = result + "`" + dollar_format.get_text() + "`"

            elif dollar_format_type == OutputFormatType.LINK:
                dollar_format = cast(OutputFormatLink, dollar_format)
                result = result + "["
                result = result + self.format_inline(this_dollar_object, dollar_format.get_children())
                result = result + "]("
                result = result + dollar_format.get_href()
                result = result + ")"

            elif dollar_format_type == OutputFormatType.DOLLAR_OBJECT:
                dollar_format = cast(OutputFormatDollarObject, dollar_format)
                dollar_object = dollar_format.get_dollar_object()
                title = dollar_object.get_id()
                if "title" in dollar_object.get_header():
                    title = dollar_object.get_header()["title"]
                result = result + "[" + title + "]("
                if self.link_type == OutputFormatDollarObjectLinkType.TO_MARKDOWN_FILE:
                    result = result + dollar_format.get_href(this_dollar_object)
                elif self.link_type == OutputFormatDollarObjectLinkType.TO_DOLLAR_ID:
                    result = result + dollar_format.get_dollar_object().get_id()
                result = result + ")"

            else:
                raise DollarExecutionException("Format {} is not supported".format(dollar_format_type))

        return result

    def format_list(self, this_dollar_object: DollarObject, dollar_formats: List[OutputFormat], ordered, context=""):
        count = 1
        result = ""
        for dollar_format in dollar_formats:
            dollar_format.validate()
            dollar_format_type = dollar_format.get_format_type()
            if dollar_format_type == OutputFormatType.LIST_ITEM:
                dollar_format = cast(OutputFormatListItem, dollar_format)
                if count > 1:
                    result = result + "\n"
                if ordered:
                    result = result + context + str(count) + ". "
                else:
                    result = result + context + "* "
                count = count + 1
                result = result + self.format_inline(this_dollar_object, dollar_format.get_children())

            elif dollar_format_type == OutputFormatType.ORDERED_LIST:
                dollar_format = cast(OutputFormatOrderedList, dollar_format)
                if count == 1:
                    raise DollarExecutionException("List can not be the first item inside a List")
                result = result + "\n" + self.format_list(
                        this_dollar_object,
                        dollar_format.get_children(),
                        True,
                        context + "    ")

            elif dollar_format_type == OutputFormatType.UNORDERED_LIST:
                dollar_format = cast(OutputFormatUnorderedList, dollar_format)
                if count == 1:
                    raise DollarExecutionException("List can not be the first item inside a List")
                result = result + "\n" + self.format_list(
                        this_dollar_object,
                        dollar_format.get_children(),
                        False,
                        context + "    ")

            else:
                raise DollarExecutionException("Format {} is not supported on List".format(dollar_format_type))

        return result
