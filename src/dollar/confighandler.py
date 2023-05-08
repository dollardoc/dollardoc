import yaml
import os

from dollar.configmap import ConfigMap
from dollar.configtype import ConfigType


class ConfigHandler:
    required_config = [
        ConfigType.DOCS_PATH,
    ]

    @classmethod
    def load_config_default(cls, path: str = "./") -> ConfigMap:
        return cls.load_config_file(os.path.join(path, "dollarconfig.yaml"))

    @classmethod
    def load_config_file(cls, path: str) -> ConfigMap:
        with open(path, "r") as f:
            config = yaml.safe_load(f.read())
            config_map = ConfigMap(config)
            config_map.validate(cls.required_config)
            return config_map
