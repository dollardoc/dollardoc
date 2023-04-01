from dollar.plugin.pluginhandler import PluginHandler
from dollar.plugin.builtin.dollarbaseextensionplugin import DollarBaseExtensionPlugin
from dollar.plugin.builtin.linkfunctionplugin import LinkFunctionPlugin
from dollar.plugin.builtin.listbacklinksfunctionplugin import ListBackLinksFunctionPlugin
from dollar.plugin.builtin.listfunctionplugin import ListFunctionPlugin
from dollar.plugin.builtin.listreffunctionplugin import ListRefFunctionPlugin
from dollar.plugin.builtin.pageextensionplugin import PageExtensionPlugin
from dollar.configmap import ConfigMap


class BuiltinPluginLoader:

    @staticmethod
    def load(config_map: ConfigMap):
        PluginHandler.register(DollarBaseExtensionPlugin(config_map))
        PluginHandler.register(LinkFunctionPlugin(config_map))
        PluginHandler.register(ListBackLinksFunctionPlugin(config_map))
        PluginHandler.register(ListFunctionPlugin(config_map))
        PluginHandler.register(ListRefFunctionPlugin(config_map))
        PluginHandler.register(PageExtensionPlugin(config_map))
