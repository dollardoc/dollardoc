from typing import List

from dollar.dollarobject import DollarObject
from dollar.plugin.plugintype import PluginType


class DollarPlugin:

    def gettype(self) -> PluginType:
        pass

    def getname(self) -> str:
        pass

class DollarFunctionPlugin(DollarPlugin):

    def gettype(self) -> PluginType:
        return PluginType.FUNCTION

    def getname(self) -> str:
        pass

    def execfunction(self, this_dollar_object: DollarObject):
        pass


class DollarBlockPlugin(DollarPlugin):

    def gettype(self) -> PluginType:
        return PluginType.BLOCK

    def getname(self) -> str:
        pass

    def execblock(self, something):
        pass



class DollarExtensionPlugin(DollarPlugin):

    def extends(self):
        return None

    def gettype(self) -> PluginType:
        return PluginType.EXTENSION

    def getname(self) -> str:
        pass

    def getsecondaries(self) -> List[str]:
        return []

    def getprimaries(self) -> List[str]:
        return []

    def execprimary(self, dollar_object):
        pass

    def execsecondary(self, dollar_object):
        pass
