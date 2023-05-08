from dollar.plugin.pluginmap import PluginMap
from dollar.plugin.builtin.dollarbaseextensionplugin import DollarBaseExtensionPlugin
from dollar.plugin.builtin.linkfunctionplugin import LinkFunctionPlugin
from dollar.plugin.builtin.listbacklinksfunctionplugin import ListBackLinksFunctionPlugin
from dollar.plugin.builtin.listfunctionplugin import ListFunctionPlugin
from dollar.plugin.builtin.listreffunctionplugin import ListRefFunctionPlugin
from dollar.plugin.builtin.pageextensionplugin import PageExtensionPlugin
from dollar.configmap import ConfigMap


class BuiltinPluginLoader:
    @staticmethod
    def load(config_map: ConfigMap, plugin_map: PluginMap):
        plugin_map.add(DollarBaseExtensionPlugin(config_map))
        plugin_map.add(LinkFunctionPlugin(config_map))
        plugin_map.add(ListBackLinksFunctionPlugin(config_map))
        plugin_map.add(ListFunctionPlugin(config_map))
        plugin_map.add(ListRefFunctionPlugin(config_map))
        plugin_map.add(PageExtensionPlugin(config_map))
