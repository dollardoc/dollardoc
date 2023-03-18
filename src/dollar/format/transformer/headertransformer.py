import copy

from dollar.dollarexecutionexception import DollarExecutionException
from dollar.dollarobjectidmap import DollarObjectIdMap


class HeaderTransformer:

    @classmethod
    def transform(cls, this_dollar_object, header):
        header = copy.deepcopy(header)
        loops = header
        if type(header) == list:
            loops = range(0, len(header))
        for key in loops:
            if key == "id" or key == "type":
                continue

            if type(header[key]) == dict:
                header[key] = cls.transform(this_dollar_object, header[key])

            elif type(header[key]) == list:
                header[key] = cls.transform(this_dollar_object, header[key])

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
                            raise DollarExecutionException("Already parsing dollar")
                        dollar_parsing = True
                        dollar_start = i
                    elif dollar_parsing:
                        if char == " ":
                            dollar_parsing = False
                            dollar_end = i - 1
                            value = cls._handlevaluestringparse(value, header, dollar_value, dollar_start, dollar_end)
                            i = dollar_end
                            dollar_value = ""
                        else:
                            dollar_value = dollar_value + char
                    i = i + 1
                if dollar_parsing:
                    if dollar_value.startswith("this."):
                        value = cls._handlevaluestringparse(value, header, dollar_value, dollar_start, len(value) - 1)
                    elif dollar_value == "this":
                        value = this_dollar_object
                    elif dollar_start == 0:
                        value = DollarObjectIdMap.get(dollar_value)
                header[key] = value

            else:
                raise DollarExecutionException("Header item of type {} not supported".format(type(header[key])))

        return header

    @classmethod
    def _handlevaluestringparse(cls, value, header, dollar_value, start, end):
        if not dollar_value.startswith("this."):
            raise DollarExecutionException("Dollar reference can only be used locally")
        dollar_key = dollar_value.removeprefix("this.")
        return value[0:start] + header[dollar_key] + value[end + 1:]