from typing import cast

from dollar.dollarexception import DollarException
from dollar.plugin.dollarplugin import DollarPlugin
from dollar.plugin.dollarplugin import DollarFunctionPlugin
from dollar.plugin.dollarplugin import DollarBlockPlugin
from dollar.plugin.dollarplugin import DollarExtensionPlugin
from dollar.plugin.plugintype import PluginType


class PluginMap:

    def __init__(self):
        self.function_map = {}
        self.block_map = {}
        self.extension_map = {}
        self.extension_secondary_map = {}

    def get_function(self, plugin_name: str) -> DollarFunctionPlugin:
        if plugin_name not in self.function_map:
            raise DollarException("Function plugin with name {}, cannot be found".format(plugin_name))
        return self.function_map[plugin_name]

    def get_block(self, plugin_name: str) -> DollarBlockPlugin:
        if plugin_name not in self.block_map:
            raise DollarException("Block plugin with name {}, cannot be found".format(plugin_name))
        return self.block_map[plugin_name]

    def get_extension(self, plugin_name) -> DollarExtensionPlugin:
        if not self.has_extension(plugin_name):
            raise DollarException("Extension plugin with name {}, cannot be found".format(plugin_name))
        return self.extension_map[plugin_name]

    def has_extension(self, plugin_name):
        if plugin_name is None:
            return False
        return plugin_name in self.extension_map

    def get_extension_from_secondary_key(self, key) -> DollarExtensionPlugin:
        if key not in self.extension_secondary_map:
            raise DollarException("No extension plugin with handler for secondary key {}".format(key))
        return self.extension_secondary_map[key]

    def has_extension_with_secondary_key(self, key) -> bool:
        return key in self.extension_secondary_map

    def add(self, plugin: DollarPlugin):
        if plugin.get_type() == PluginType.FUNCTION:
            plugin = cast(DollarFunctionPlugin, plugin)
            self.function_map[plugin.get_name()] = plugin
        elif plugin.get_type() == PluginType.BLOCK:
            plugin = cast(DollarBlockPlugin, plugin)
            self.block_map[plugin.get_name()] = plugin
        elif plugin.get_type() == PluginType.EXTENSION:
            plugin = cast(DollarExtensionPlugin, plugin)
            self.extension_map[plugin.get_name()] = plugin
            for secondary in plugin.get_secondaries():
                self.extension_secondary_map[secondary] = plugin
        else:
            raise DollarException("Plugin with type {} is not supported".format(plugin.get_type()))

    def _copy(self) -> "PluginMap":
        new_function_map = {}
        new_block_map = {}
        new_extension_map = {}
        new_extension_secondary_map = {}
        for key in self.function_map:
            new_function_map[key] = self.function_map[key]
        for key in self.block_map:
            new_block_map[key] = self.block_map[key]
        for key in self.extension_map:
            new_extension_map[key] = self.extension_map[key]
        for key in self.extension_secondary_map:
            new_extension_secondary_map[key] = self.extension_secondary_map[key]
        plugin_map = PluginMap()
        plugin_map.function_map = new_function_map
        plugin_map.block_map = new_block_map
        plugin_map.extension_map = new_extension_map
        plugin_map.extension_secondary_map = new_extension_secondary_map
        return plugin_map

