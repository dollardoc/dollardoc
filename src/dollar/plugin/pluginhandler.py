import os
import importlib.util
import inspect

from dollar.plugin.dollarplugin import DollarPlugin
from dollar.plugin.pluginmap import PluginMap
from dollar.configmap import ConfigMap


class PluginHandler:

    plugin_map = PluginMap()

    @classmethod
    def _import_plugin_path(cls, path, plugin_map: PluginMap, config_map: ConfigMap):
        spec = importlib.util.spec_from_file_location(path, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for key in module.__dict__:
            if inspect.isclass(module.__dict__[key]) and issubclass(module.__dict__[key], DollarPlugin):
                plugin_map.add(module.__dict__[key](config_map))

    @classmethod
    def import_plugins(cls, path: str, config_map: ConfigMap) -> PluginMap:
        plugin_map = cls.plugin_map._copy()
        cls._import_plugins(os.path.join(os.path.curdir, path), plugin_map, config_map)
        return plugin_map

    @classmethod
    def _import_plugins(cls, abs_path, plugin_map: PluginMap, config_map: ConfigMap):
        dir_list = os.listdir(abs_path)
        for item in dir_list:
            new_path = os.path.join(abs_path, item)
            if os.path.isdir(new_path):
                cls._import_plugins(new_path, plugin_map, config_map)
            elif item.endswith(".py"):
                cls._import_plugin_path(new_path, plugin_map, config_map)

    @classmethod
    def register(cls, plugin: DollarPlugin):
        cls.plugin_map.add(plugin)
