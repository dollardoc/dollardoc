import yaml

from dollar.dollarexception import DollarExecutionException
from dollar.dollarcontext import DollarContext
from dollar.format.header.headerparserresult import HeaderParserResult


class HeaderParser:

    @classmethod
    def parse(cls, content, dollar_context: DollarContext):
        content = content.split("\n")
        result = HeaderParserResult(None, 0)

        started_headers = False
        first_line = True
        first_line_in_header = True
        header = ""
        for i in range(0, len(content)):
            line = content[i]

            if line.rstrip() == "---":
                first_line = False
                if started_headers:
                    started_headers = False
                    result.header_end = i
                    break
                else:
                    started_headers = True

            elif first_line:
                if line.strip() != "":
                    break

            else:
                if first_line_in_header:
                    first_line_in_header = False
                else:
                    header = header + "\n"
                header = header + line

        if started_headers:
            raise DollarExecutionException(
                    "Parsing headers exited with a faulty state",
                    dollar_context)

        result.header_object = yaml.safe_load(header)
        return result
