from typing import List
from typing import Optional

from dollar.dollarobject import DollarObject
from dollar.plugin.plugintype import PluginType
from dollar.plugin.pluginarg import PluginArg


class DollarPlugin:

    def get_type(self) -> PluginType:
        pass

    def get_name(self) -> str:
        pass


class DollarFunctionPlugin(DollarPlugin):

    def get_type(self) -> PluginType:
        return PluginType.FUNCTION

    def get_arg_info(self) -> List[PluginArg]:
        return []

    def get_name(self) -> str:
        pass

    def exec_function(self, this_dollar_object: DollarObject):
        pass


class DollarBlockPlugin(DollarPlugin):

    def get_type(self) -> PluginType:
        return PluginType.BLOCK

    def get_name(self) -> str:
        pass

    def exec_block(self, something):
        pass


class DollarExtensionPlugin(DollarPlugin):

    def extends(self):
        return None

    def get_type(self) -> PluginType:
        return PluginType.EXTENSION

    def get_name(self) -> str:
        pass

    def validate_primary(self, dollar_object: DollarObject) -> Optional[str]:
        return None

    def get_secondaries(self) -> List[str]:
        return []

    def get_primaries(self) -> List[str]:
        return []

    def exec_primary(self, dollar_object):
        pass

    def exec_secondary(self, dollar_object):
        pass
