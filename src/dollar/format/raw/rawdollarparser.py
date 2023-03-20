from dollar.dollarexception import DollarExecutionException
from dollar.dollarcontext import DollarContext
from dollar.dollarcontext import DollarContextSpan
from dollar.format.raw.rawdollarformat import RawDollarFormatText
from dollar.format.raw.rawdollarformat import RawDollarFormatReference
from dollar.format.raw.rawdollarformat import RawDollarFormatFunction
from dollar.format.raw.rawdollarformat import RawDollarFormatBlock
from dollar.format.raw.rawdollarformat import RawDollarFormatUnion


class RawDollarParser:

    @classmethod
    def parse(cls, raw_content: str, dollar_context_start: DollarContext):
        dollar_count = 0
        dollar_open = 0
        quotes = False
        parenteses = 0
        result = []
        text = ""
        last_char = ""
        file = dollar_context_start.get_file()
        line = dollar_context_start.get_line()
        col = dollar_context_start.get_col()
        last_col = dollar_context_start.get_col()
        dollar_context_start = None
        for i in range(0, len(raw_content)):
            col = col + 1
            if dollar_context_start is None:
                dollar_context_start = DollarContext(file, line, col)
            char = raw_content[i]
            if char == "\n":
                line = line + 1
                last_col = col - 1
                col = 0
            escape = False
            if last_char == "\\":
                escape = True
                if char == "\\":
                    text = text + "\\"
                    last_char = char
                    continue
            if char == "$" and not escape and not quotes:
                if dollar_open == 3 and raw_content[i+1] != "$" and dollar_count != 2:
                    text = text + "$"
                elif dollar_open not in (0, 3):
                    text = text + "$"
                    last_char = char
                    continue
                dollar_count = dollar_count + 1
                if dollar_open == 0 and text != "":
                    dollar_context = DollarContextSpan(
                            dollar_context_start,
                            DollarContext(file, line, col))
                    result.append(cls._create_result_text(text, dollar_context))
                    text = ""
                    dollar_context_start = None
                if dollar_open == dollar_count:
                    if dollar_open == 3:
                        dollar_context = DollarContextSpan(
                                dollar_context_start,
                                DollarContext(file, line, col))
                        result.append(cls._create_result_block(text, dollar_context))
                        text = ""
                        dollar_context_start = None
                    dollar_open = 0
                    dollar_count = 0
            elif char != "\\":
                if dollar_count != 0 and dollar_open == 0:
                    dollar_open = dollar_count
                dollar_count = 0
                if dollar_open in (0, 3):
                    text = text + char
                else:
                    if char == "(":
                        parenteses = parenteses + 1
                    elif char == ")":
                        parenteses = parenteses - 1
                    elif char == "\"" and not escape:
                        quotes = not quotes
                    if char in (" ", "\n") and not escape and not quotes and not parenteses > 0:
                        temp_line = line
                        temp_col = col
                        if col == 0:
                            temp_line = temp_line - 1
                            temp_col = last_col
                        dollar_context = DollarContextSpan(
                                dollar_context_start,
                                DollarContext(file, temp_line, temp_col))
                        if dollar_open == 1:
                            dollar_text = text
                            continue_text = ""
                            if dollar_text[-1] in (".", ",", ":", ";", "!", "?"):
                                continue_text = dollar_text[-1]
                                dollar_text = dollar_text[:-1]
                            result.append(cls._create_result_reference(dollar_text, dollar_context))
                            dollar_open = 0

                            text = continue_text
                            dollar_context_start = DollarContext(file, line, col)
                        elif dollar_open == 2:
                            result.append(cls._create_result_function(text, dollar_context))
                            dollar_open = 0
                            text = ""
                            dollar_context_start = DollarContext(file, line, col)
                    text = text + char
            last_char = char
        if text != "":
            dollar_context = DollarContextSpan(
                    dollar_context_start,
                    DollarContext(file, line, col))
            if dollar_open == 0:
                result.append(cls._create_result_text(text, dollar_context))
            elif dollar_open == 1:
                result.append(cls._create_result_reference(text, dollar_context))
            elif dollar_open == 2:
                result.append(cls._create_result_function(text, dollar_context))
        return result

    @classmethod
    def _create_result_function(cls, text, dollar_context: DollarContext):
        text_split = text.split("(")
        if len(text_split) != 2:
            raise DollarExecutionException("Dollar Function is not formatted properly", dollar_context)
        func_name = text_split[0]
        param_str = text_split[1].split(")")[0]
        col_start_diff = dollar_context.get_col() + len(func_name) + 2
        param_str_split = param_str.split(",")
        params = []
        if len(param_str_split) == 1 and param_str_split[0] == "":
            pass
        else:
            first_param = True
            for param in param_str_split:
                if not first_param:
                    col_start_diff = col_start_diff + 1
                first_param = False
                dollar_context_param_start = DollarContext(
                        dollar_context.get_file(),
                        dollar_context.get_line(),
                        col_start_diff)
                param_content = cls.parse(param, dollar_context_param_start)
                if len(param_content) == 0:
                    dollar_context_param = DollarContextSpan(
                            dollar_context_param_start,
                            DollarContext(
                                    dollar_context.get_file(),
                                    dollar_context.get_line(),
                                    col_start_diff + len(param)))
                    raise DollarExecutionException(
                            "Parameter on {} cant be empty".format(func_name),
                            dollar_context_param)
                if len(param_content) == 1:
                    params.append(param_content[0])
                else:
                    params.append(RawDollarFormatUnion(param_content, dollar_context))
                col_start_diff = col_start_diff + len(param)
        return RawDollarFormatFunction(func_name, params, dollar_context)

    @classmethod
    def _create_result_text(cls, text, dollar_context: DollarContext):
        return RawDollarFormatText(text, dollar_context)

    @classmethod
    def _create_result_reference(cls, text, dollar_context: DollarContext):
        if text[0] == "(" and text[-1] == ")":
            text = text[1:-1]
        return RawDollarFormatReference(text, dollar_context)

    @classmethod
    def _create_result_block(cls, text, dollar_context: DollarContextSpan):
        text_split = text.split("\n")
        plugin_name = text_split[0].strip()
        text_split = text_split[1:]
        contains_tab = True
        for t in text_split:
            if t.strip() != "" and not t.startswith("    "):
                contains_tab = True
        text_split_new = []
        for t in text_split:
            if t.strip() != "":
                if contains_tab:
                    t = t.removeprefix("    ")
                text_split_new.append(t)
        dollar_context_content = DollarContext(
                dollar_context.get_context_start().get_file(),
                dollar_context.get_context_start().get_line() + 1,
                0)
        plugin_content = cls.parse("\n".join(text_split_new), dollar_context_content)
        dollar_context_union = DollarContextSpan(
                DollarContext(
                        dollar_context.get_context_start().get_file(),
                        dollar_context.get_context_start().get_line() + 1,
                        1),
                DollarContext(
                        dollar_context.get_context_end().get_file(),
                        dollar_context.get_context_end().get_line() - 1,
                        len(text_split_new[-1]) + 1)
        )
        return RawDollarFormatBlock(
                plugin_name,
                RawDollarFormatUnion(plugin_content, dollar_context_union),
                dollar_context)
