from dollar.plugin.pluginhandler import PluginHandler
from dollar.plugin.builtin.linkfunctionplugin import LinkFunctionPlugin
from dollar.plugin.builtin.listbacklinksfunctionplugin import ListBackLinksFunctionPlugin
from dollar.plugin.builtin.listfunctionplugin import ListFunctionPlugin
from dollar.plugin.builtin.listreffunctionplugin import ListRefFunctionPlugin
from dollar.plugin.builtin.pageextensionplugin import PageExtensionPlugin


class BuiltinPluginLoader:

    @staticmethod
    def load():
        PluginHandler.register(LinkFunctionPlugin())
        PluginHandler.register(ListBackLinksFunctionPlugin())
        PluginHandler.register(ListFunctionPlugin())
        PluginHandler.register(ListRefFunctionPlugin())
        PluginHandler.register(PageExtensionPlugin())
