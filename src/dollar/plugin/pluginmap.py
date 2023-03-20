from typing import cast

from dollar.dollarexception import DollarException
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
    def get_function(cls, plugin_name: str) -> DollarFunctionPlugin:
        if plugin_name not in cls.function_map:
            raise DollarException("Function plugin with name {}, cannot be found".format(plugin_name))
        return cls.function_map[plugin_name]

    @classmethod
    def get_block(cls, plugin_name: str) -> DollarBlockPlugin:
        if plugin_name not in cls.block_map:
            raise DollarException("Block plugin with name {}, cannot be found".format(plugin_name))
        return cls.block_map[plugin_name]

    @classmethod
    def get_extension(cls, plugin_name) -> DollarExtensionPlugin:
        if not cls.has_extension(plugin_name):
            raise DollarException("Extension plugin with name {}, cannot be found".format(plugin_name))
        return cls.extension_map[plugin_name]

    @classmethod
    def has_extension(cls, plugin_name):
        return plugin_name in cls.extension_map

    @classmethod
    def get_extension_from_secondary_key(cls, key) -> DollarExtensionPlugin:
        if key not in cls.extension_secondary_map:
            raise DollarException("No extension plugin with handler for secondary key {}".format(key))
        return cls.extension_secondary_map[key]

    @classmethod
    def has_extension_with_secondary_key(cls, key) -> bool:
        return key in cls.extension_secondary_map

    @classmethod
    def add(cls, plugin: DollarPlugin):
        if plugin.get_type() == PluginType.FUNCTION:
            plugin = cast(DollarFunctionPlugin, plugin)
            cls.function_map[plugin.get_name()] = plugin
        elif plugin.get_type() == PluginType.BLOCK:
            plugin = cast(DollarBlockPlugin, plugin)
            cls.block_map[plugin.get_name()] = plugin
        elif plugin.get_type() == PluginType.EXTENSION:
            plugin = cast(DollarExtensionPlugin, plugin)
            cls.extension_map[plugin.get_name()] = plugin
            for secondary in plugin.get_secondaries():
                cls.extension_secondary_map[secondary] = plugin
        else:
            raise DollarException("Plugin with type {} is not supported".format(plugin.get_type()))

    @classmethod
    def clean(cls):
        cls.function_map = {}
        cls.block_map = {}
        cls.extension_map = {}
        cls.extension_secondary_map = {}

