from dollar.dollarexecutionexception import DollarExecutionException
from dollar.format.raw.rawdollarformat import RawDollarFormatText
from dollar.format.raw.rawdollarformat import RawDollarFormatReference
from dollar.format.raw.rawdollarformat import RawDollarFormatFunction
from dollar.format.raw.rawdollarformat import RawDollarFormatBlock
from dollar.format.raw.rawdollarformat import RawDollarFormatUnion


class RawDollarParser:

    @classmethod
    def parse(cls, raw_content: str):
        dollar_count = 0
        dollar_open = 0
        quotes = False
        escape = False
        parenteses = 0
        result = []
        text = ""
        last_char = ""
        for i in range(0, len(raw_content)):
            char = raw_content[i]
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
                    result.append(cls._createresulttext(text))
                    text = ""
                if dollar_open == dollar_count:
                    if dollar_open == 3:
                        result.append(cls._createresultblock(text))
                        text = ""
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
                        if dollar_open == 1:
                            result.append(cls._createresultreference(text))
                        elif dollar_open == 2:
                            result.append(cls._createresultfunction(text))
                        dollar_open = 0
                        text = ""
                    text = text + char
            last_char = char
        if text != "":
            if dollar_open == 0:
                result.append(cls._createresulttext(text))
            elif dollar_open == 1:
                result.append(cls._createresultreference(text))
            elif dollar_open == 2:
                result.append(cls._createresultfunction(text))
        return result

    @classmethod
    def _createresultfunction(cls, text):
        text_split = text.split("(")
        if len(text_split) != 2:
            raise DollarExecutionException("Dollar Function is not formatted properly")
        func_name = text_split[0]
        param_str = text_split[1].split(")")[0]
        params = []
        for param in param_str.split(","):
            param_content = cls.parse(param)
            if len(param_content) == 0:
                raise DollarExecutionException("Parameter on {} cant be empty".format(func_name))
            if len(param_content) == 1:
                params.append(param_content[0])
            else:
                params.append(RawDollarFormatUnion(param_content))
        return RawDollarFormatFunction(func_name, params)

    @classmethod
    def _createresulttext(cls, text):
        return RawDollarFormatText(text)

    @classmethod
    def _createresultreference(cls, text):
        if text[0] == "(" and text[-1] == ")":
            text = text[1:-1]
        return RawDollarFormatReference(text)

    @classmethod
    def _createresultblock(cls, text):
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
        plugin_content = cls.parse("\n".join(text_split_new))
        return RawDollarFormatBlock(plugin_name, RawDollarFormatUnion(plugin_content))
