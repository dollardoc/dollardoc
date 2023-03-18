import os
import importlib.util

from dollar.plugin.dollarplugin import DollarPlugin
from dollar.plugin.pluginmap import PluginMap


class PluginHandler:

    @classmethod
    def _importpluginpath(cls, path):
        spec = importlib.util.spec_from_file_location(path, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    @classmethod
    def importplugins(cls, path):
        cls._importplugins(os.path.join(os.path.curdir, path))

    @classmethod
    def _importplugins(cls, abs_path):
        dir_list = os.listdir(abs_path)
        for item in dir_list:
            new_path = os.path.join(abs_path, item)
            if os.path.isdir(new_path):
                cls.importplugins(new_path)
            elif item.endswith(".py"):
                cls._importpluginpath(new_path)

    @classmethod
    def register(cls, plugin: DollarPlugin):
       PluginMap.add(plugin)

