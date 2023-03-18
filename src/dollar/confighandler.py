import yaml


class ConfigHandler:
    config = {}

    @classmethod
    def setconfig(cls, config):
        cls.config = config

    @classmethod
    def get(cls, key):
        return cls.config[key]

    @classmethod
    def load_config_default(cls):
        cls.load_config_file("dollarconfig.yaml")

    @classmethod
    def load_config_file(cls, path):
        with open(path, "r") as f:
            cls.config = yaml.safe_load(f.read())


    @classmethod
    def getpluginconfig(cls, plugin_name):
        if "plugin" not in cls.config:
            return None
        if plugin_name not in cls.config["plugin"]:
            return None
        return cls.config["plugin"][plugin_name]
