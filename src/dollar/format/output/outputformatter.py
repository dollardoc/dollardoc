from typing import List

from dollar.dollarexecutionexception import DollarExecutionException
from dollar.dollarobject import DollarObject
from dollar.format.output.outputformat import _OutputFormat
from dollar.format.output.outputformattype import OutputFormatType


class OutputFormatterMarkdown:

    @classmethod
    def format(cls, this_dollar_object: DollarObject, dollar_formats: List[_OutputFormat], context=""):
        result = []
        for dollar_format in dollar_formats:
            dollar_format.validate()
            dollar_format_type = dollar_format.getformattype()
            if not dollar_format.isblock():
                raise DollarExecutionException("{} is not allowed as a root level block".format(dollar_format.getformattype()))

            if dollar_format_type == OutputFormatType.HEADER:
                head = ""
                for i in range(0, dollar_format.getlevel()):
                    head = head + "#"
                result.append(context + head + " " + cls.format_inline(this_dollar_object, dollar_format.getchildren(), context))

            elif dollar_format_type == OutputFormatType.PARAGRAPH:
                result.append(context + cls.format_inline(this_dollar_object, dollar_format.getchildren(), context))

            elif dollar_format_type == OutputFormatType.ORDERED_LIST:
                result.append(context + cls.format_list(this_dollar_object, dollar_format.getchildren(), True, context))

            elif dollar_format_type == OutputFormatType.UNORDERED_LIST:
                result.append(context + cls.format_list(this_dollar_object, dollar_format.getchildren(), False, context))

            elif dollar_format_type == OutputFormatType.CODE_BLOCK:
                join_str = "\n" + context
                text = join_str.join(dollar_format.gettext().split("\n"))
                result.append(context + "``` " + dollar_format.getcodetype() + "\n" + context + text + "\n" + context + "```")

            elif dollar_format_type == OutputFormatType.QUOTE_BLOCK:
                result.append(cls.format(this_dollar_object, dollar_format.getchildren(), context + "> "))

            elif dollar_format_type == OutputFormatType.DEFINITION:
                result.append(context + cls.format_inline(this_dollar_object, dollar_format.getdefinedchildren(), context)
                        + "\n" + context + ": " + cls.format_inline(this_dollar_object, dollar_format.getdefinitionchildren(), context))

            elif dollar_format_type == OutputFormatType.PLUGIN_BLOCK:
                join_str = "\n" + context
                text = join_str.join(dollar_format.gettext().split("\n"))
                result.append(context + "``` " + dollar_format.getpluginname() + "\n" + context + text + "\n" + context + "```")

            else:
                raise DollarExecutionException("{} is not allowed as a root level block".format(dollar_format.getformattype()))

        join_str = "\n" + context + "\n"
        return join_str.join(result)

    @classmethod
    def format_inline(cls, this_dollar_object: DollarObject, dollar_formats: List[_OutputFormat], context=""):
        result = ""
        for dollar_format in dollar_formats:
            dollar_format.validate()
            dollar_format_type = dollar_format.getformattype()
            if dollar_format.isblock():
                raise DollarExecutionException("{} is not allowed as a nested inline item".format(dollar_format.getformattype()))

            if dollar_format_type == OutputFormatType.TEXT:
                result = result + dollar_format.gettext()

            elif dollar_format_type == OutputFormatType.BOLD:
                result = result + "**" + cls.format_inline(this_dollar_object, dollar_format.getchildren()) + "**"

            elif dollar_format_type == OutputFormatType.ITALIC:
                result = result + "*" + cls.format_inline(this_dollar_object, dollar_format.getchildren()) + "*"

            elif dollar_format_type == OutputFormatType.CODE:
                result = result + "`" + dollar_format.gettext() + "`"

            elif dollar_format_type == OutputFormatType.LINK:
                result = result + "[" + cls.format_inline(this_dollar_object, dollar_format.getchildren()) + "](" + dollar_format.gethref() + ")"

            elif dollar_format_type == OutputFormatType.DOLLAR_OBJECT:
                dollar_object = dollar_format.getdollarobject()
                title = dollar_object.getid()
                if "title" in dollar_object.getheader():
                    title = dollar_object.getheader()["title"]
                result = result + "[" + title + "](" + dollar_format.gethref(this_dollar_object) + ")"

            else:
                raise DollarExecutionException("Format {} is not supported".format(dollar_format_type))

        return result

    @classmethod
    def format_list(cls, this_dollar_object: DollarObject, dollar_formats: List[_OutputFormat], ordered, context=""):
        count = 1
        result = ""
        for dollar_format in dollar_formats:
            dollar_format.validate()
            dollar_format_type = dollar_format.getformattype()
            if dollar_format_type == OutputFormatType.LIST_ITEM:
                if count > 1:
                    result = result + "\n"
                if ordered:
                    result = result + context + str(count) + ". "
                else:
                    result = result + context + "* "
                count = count + 1
                result = result + cls.format_inline(this_dollar_object, dollar_format.getchildren(), context + "    ")

            elif dollar_format_type == OutputFormatType.ORDERED_LIST:
                if count == 1:
                    raise DollarExecutionException("List can not be the first item inside a List")
                result = result + "\n" + cls.format_list(this_dollar_object, dollar_format.getchildren(), True, context + "    ")

            elif dollar_format_type == OutputFormatType.UNORDERED_LIST:
                if count == 1:
                    raise DollarExecutionException("List can not be the first item inside a List")
                result = result + "\n" + cls.format_list(dollar_format.getchildren(), False, context + "    ")

            else:
                raise DollarExecutionException("Format {} is not supported on List".format(dollar_format_type))

        return result
