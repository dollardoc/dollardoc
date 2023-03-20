from typing import Optional

from dollar.dollarobject import DollarObject


class PluginArg:

    def __init__(self, name: str, arg_type, description: str):
        self.name = name
        self.arg_type = arg_type
        self.description = description

    def get_name(self):
        return self.name

    def get_arg_type(self):
        return self.arg_type

    def get_description(self):
        return self.description


class PluginArgDollarObject(PluginArg):

    def __init__(self, dollar_object_type: Optional[str], description: str):
        super().__init__("dollar_object", DollarObject, description)
        self.dollar_object_type = dollar_object_type

    def get_dollar_object_type(self) -> Optional[str]:
        return self.dollar_object_type
