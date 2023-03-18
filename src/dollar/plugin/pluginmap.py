from dollar.dollarexecutionexception import DollarExecutionException
from dollar.plugin.dollarplugin import DollarPlugin
from dollar.plugin.dollarplugin import DollarFunctionPlugin
from dollar.plugin.dollarplugin import DollarBlockPlugin
from dollar.plugin.dollarplugin import DollarExtensionPlugin
from dollar.plugin.plugintype import PluginType


class PluginMap:

    function_map = {}
    block_map = {}
    extension_map = {}
    extension_secondary_map = {}

    @classmethod
    def getfunction(cls, plugin_name: str) -> DollarFunctionPlugin:
        if plugin_name not in cls.function_map:
            DollarExecutionException("Function plugin with name {}, cannot be found".format(plugin_name))
        return cls.function_map[plugin_name]

    @classmethod
    def getblock(cls, plugin_name: str) -> DollarBlockPlugin:
        if plugin_name not in cls.block_map:
            DollarExecutionException("Block plugin with name {}, cannot be found".format(plugin_name))
        return cls.block_map[plugin_name]

    @classmethod
    def getextension(cls, plugin_name) -> DollarExtensionPlugin:
        if not cls.hasextension(plugin_name):
            DollarExecutionException("Extension plugin with name {}, cannot be found".format(plugin_name))
        return cls.extension_map[plugin_name]

    @classmethod
    def hasextension(cls, plugin_name):
        return plugin_name in cls.extension_map

    @classmethod
    def getextensionfromsecondarykey(cls, key) -> DollarExtensionPlugin:
        if key not in cls.extension_secondary_map:
            DollarExecutionException("No extension plugin with handler for secondary key {}".format(key))
        return cls.extension_secondary_map[key]

    @classmethod
    def hasextensionwithsecondarykey(cls, key) -> bool:
        return key in cls.extension_secondary_map

    @classmethod
    def add(cls, plugin: DollarPlugin):
        if plugin.gettype() == PluginType.FUNCTION:
            cls.function_map[plugin.getname()] = plugin
        elif plugin.gettype() == PluginType.BLOCK:
            cls.block_map[plugin.getname()] = plugin
        elif plugin.gettype() == PluginType.EXTENSION:
            cls.extension_map[plugin.getname()] = plugin
            for secondary in plugin.getsecondaries():
                cls.extension_secondary_map[secondary] = plugin
        else:
            DollarExecutionException("Plugin with type {} is not supported".format(plugin.gettype()))

