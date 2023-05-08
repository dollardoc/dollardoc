import os
import importlib.util
import inspect

from dollar.plugin.builtinpluginloader import BuiltinPluginLoader
from dollar.plugin.dollarplugin import DollarPlugin
from dollar.plugin.pluginmap import PluginMap
from dollar.configmap import ConfigMap


class PluginHandler:

    @classmethod
    def _import_plugin_path(cls, path, plugin_map: PluginMap, config_map: ConfigMap):
        spec = importlib.util.spec_from_file_location(path, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        skip = 0
        for key in module.__dict__:
            if inspect.isclass(module.__dict__[key]) and issubclass(module.__dict__[key], DollarPlugin):
                instance = module.__dict__[key](config_map)
                if instance.get_name() is not None:
                    plugin_map.add(instance)

    @classmethod
    def import_plugins(cls, path: str, config_map: ConfigMap) -> PluginMap:
        plugin_map = PluginMap()
        BuiltinPluginLoader.load(config_map, plugin_map)
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
