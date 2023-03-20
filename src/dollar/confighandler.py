import yaml
from enum import Enum

from dollar.dollarexception import DollarExecutionException


class ConfigType(str, Enum):
    DOCS_PATH = "docs_path"  # str
    TARGET_PATH = "target_path"  # str
    PLUGIN_PATH = "plugin_path"  # str
    FILE_PASSTHROUGH = "file_passthrough"  # List[str]


class ConfigHandler:
    config = {}
    required_config = [
        ConfigType.DOCS_PATH,
    ]

    @classmethod
    def set_config(cls, config):
        cls.config = config
        cls.validate()

    @classmethod
    def get(cls, key):
        if type(key) == str:
            raise DollarExecutionException("Keys must be provided in type ConfigType")
        if key not in cls.config:
            raise DollarExecutionException("Key {} was not provided in config".format(key))
        return cls.config[key]

    @classmethod
    def get_str_list(cls, key):
        value = cls.get(key)
        if type(value) == str:
            return [value]
        elif type(value) == list:
            return value
        else:
            raise DollarExecutionException("Key {} was not list or string as expected".format(key))

    @classmethod
    def get_opt(cls, key, default):
        if type(key) == str:
            raise DollarExecutionException("Keys must be provided in type ConfigType")
        if key in cls.config:
            return cls.config[key]
        return default

    @classmethod
    def get_str_list_opt(cls, key):
        value = cls.get_opt(key, [])
        if type(value) == str:
            return [value]
        elif type(value) == list:
            return value
        else:
            raise DollarExecutionException("Key {} was not list or string as expected".format(key))

    @classmethod
    def load_config_default(cls):
        cls.load_config_file("dollarconfig.yaml")

    @classmethod
    def load_config_file(cls, path):
        with open(path, "r") as f:
            cls.config = yaml.safe_load(f.read())
        cls.validate()

    @classmethod
    def get_plugin_config(cls, plugin_name):
        if "plugin" not in cls.config:
            return None
        if plugin_name not in cls.config["plugin"]:
            return None
        return cls.config["plugin"][plugin_name]

    @classmethod
    def validate(cls):
        for req in cls.required_config:
            if req not in cls.config:
                raise DollarExecutionException("Required config {} not present in config".format(req))
