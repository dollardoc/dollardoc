from enum import Enum


class ConfigType(str, Enum):
    DOCS_PATH = "docs_path"  # str
    TARGET_PATH = "target_path"  # str
    PLUGIN_PATH = "plugin_path"  # str
    FILE_PASSTHROUGH = "file_passthrough"  # List[str]
