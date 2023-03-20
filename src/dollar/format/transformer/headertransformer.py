import copy

from dollar.dollarexception import DollarExecutionException
from dollar.dollarexception import DollarException
from dollar.dollarcontext import DollarContext
from dollar.dollarobject import DollarObject
from dollar.dollarobjectidmap import DollarObjectIdMap


class HeaderTransformer:

    @classmethod
    def transform(cls, this_dollar_object: DollarObject, header, dollar_context: DollarContext):
        header = copy.deepcopy(header)
        loops = header
        if type(header) == list:
            loops = range(0, len(header))
        for key in loops:
            if key == "id" or key == "type":
                continue

            if type(header[key]) == dict:
                header[key] = cls.transform(this_dollar_object, header[key], dollar_context)

            elif type(header[key]) == list:
                header[key] = cls.transform(this_dollar_object, header[key], dollar_context)

            elif type(header[key]) == str:
                value = header[key].strip()

                dollar_parsing = False
                dollar_start = 0
                dollar_value = ""
                i = 0
                while i < len(value):
                    char = value[i]
                    if char == "$":
                        if dollar_parsing:
                            raise DollarExecutionException("Already parsing dollar", dollar_context)
                        dollar_parsing = True
                        dollar_start = i
                    elif dollar_parsing:
                        if char == " ":
                            dollar_parsing = False
                            dollar_end = i - 1
                            value = cls._handle_value_string_parse(
                                    value,
                                    header,
                                    dollar_value,
                                    dollar_start,
                                    dollar_end,
                                    dollar_context)
                            i = dollar_end
                            dollar_value = ""
                        else:
                            dollar_value = dollar_value + char
                    i = i + 1
                if dollar_parsing:
                    if dollar_value.startswith("this."):
                        value = cls._handle_value_string_parse(
                                value,
                                header,
                                dollar_value,
                                dollar_start,
                                len(value) - 1,
                                dollar_context)
                    elif dollar_value == "this":
                        value = this_dollar_object
                    elif dollar_start == 0:
                        try:
                            value = DollarObjectIdMap.get(dollar_value)
                        except DollarException as e:
                            raise DollarExecutionException(
                                    e.get_message(),
                                    dollar_context) from e

                header[key] = value

            else:
                raise DollarExecutionException(
                        "Header item of type {} not supported".format(type(header[key])),
                        dollar_context)

        return header

    @classmethod
    def _handle_value_string_parse(cls, value, header, dollar_value, start, end, dollar_context):
        if not dollar_value.startswith("this."):
            raise DollarExecutionException("Dollar reference can only be used locally", dollar_context)
        dollar_key = dollar_value.removeprefix("this.")
        return value[0:start] + header[dollar_key] + value[end + 1:]
