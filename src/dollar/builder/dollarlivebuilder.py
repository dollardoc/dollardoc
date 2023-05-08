import os
from typing import List

from dollar.configmap import ConfigMap
from dollar.configtype import ConfigType
from dollar.plugin.pluginhandler import PluginHandler
from dollar.file.dollarfile import DollarFile
from dollar.file.dollarfilereader import DollarFileReader
from dollar.file.dollarfilewriter import DollarFileWriter
from dollar.dollarobjectidmap import DollarObjectIdMap
from dollar.helper.dollarobjectcreationhelper import DollarObjectCreationHelper
from dollar.dollarobjectidmap import DollarObjectIdMapDiff
from dollar.dollarcontext import DollarContext
from dollar.format.output.outputformatter import OutputFormatterMarkdown
from dollar.format.output.outputformatdollarobjectlinktype import OutputFormatDollarObjectLinkType
from dollar.format.raw.rawdollarparser import RawDollarParser
from dollar.format.transformer.inputtostrtransformer import InputToStrTransformer
from dollar.format.transformer.rawtoinputtransformer import RawToInputTransformer


class DollarLiveBuilder:

    def __init__(self, base_path:str, config_map: ConfigMap):
        self.output_formatter = OutputFormatterMarkdown(OutputFormatDollarObjectLinkType.TO_DOLLAR_ID)
        self.config_map = config_map
        self.conf_docs_path = os.path.join(base_path, self.config_map.get(ConfigType.DOCS_PATH))
        self.conf_target_path = os.path.join(base_path, self.config_map.get(ConfigType.TARGET_PATH))
        self.conf_plugin_path = os.path.join(base_path, self.config_map.get(ConfigType.PLUGIN_PATH))
        self.conf_file_passthrough = self.config_map.get_str_list_opt(ConfigType.FILE_PASSTHROUGH)
        self.plugin_map = PluginHandler.import_plugins(self.conf_plugin_path, self.config_map)
        self.dollar_id_map = None
        self.loaded_dollar_id_map = None
        self.loaded_dollar_objects = []
        self.dollar_objects = []
        self.dollar_files = {
            "all_files": [],
            "mdd_files": [],
        }

    def load_files(self):
        all_dollar_files = self._read_all_files()
        mdd_dollar_files = [df for df in all_dollar_files if df.is_file_ending("mdd")]
        self.dollar_files["all_files"] = all_dollar_files
        self.dollar_files["mdd_files"] = mdd_dollar_files

    def _read_all_files(self) -> List[DollarFile]:
        return DollarFileReader.read_files(self.conf_docs_path)

    def load_dollar(self) -> DollarObjectIdMapDiff:
        dollar_objects = []
        dollar_id_map = DollarObjectIdMap()
        for mdd_file in self.dollar_files["mdd_files"]:
            path = mdd_file.get_path()
            content = mdd_file.get_content()
            dollar_object = DollarObjectCreationHelper.init(path, content, dollar_id_map)
            dollar_objects.append(dollar_object)
        if self.loaded_dollar_id_map != None:
            dollar_id_map_diff = self.loaded_dollar_id_map.diff(dollar_id_map)
            if dollar_id_map_diff.is_changed():
                return dollar_id_map_diff
        else:
            dollar_id_map_diff = DollarObjectIdMapDiff([], [], [])
        self.loaded_dollar_id_map = dollar_id_map
        return dollar_id_map_diff

    def apply_loaded_dollar(self):
        self.dollar_id_map = self.loaded_dollar_id_map.copy()

    def apply_single_dollar(self, dollar_object):
        self.dollar_id_map.add__force(dollar_object)

    def load_dollar_headers(self):
        for dollar_object_id, dollar_object in self.dollar_id_map.get_map().items():
            DollarObjectCreationHelper.transform_header_primary(dollar_object, self.dollar_id_map, self.plugin_map)
        for dollar_object_id, dollar_object in self.dollar_id_map.get_map().items():
            DollarObjectCreationHelper.transform_header_secondary(dollar_object, self.dollar_id_map, self.plugin_map)



    def build_partial(self, dollar_object_id, content):
        dollar_object = self.dollar_id_map.get(dollar_object_id)
        dollar_context_start = DollarContext(
                dollar_object.get_path(),
                0,
                0)
        dollar_raw = RawDollarParser.parse(
                content,
                dollar_context_start)

        input_formats = RawToInputTransformer.transform_list(
                dollar_object,
                dollar_raw,
                self.dollar_id_map,
                self.plugin_map)

        output_content = InputToStrTransformer.transform_list(
                self.output_formatter,
                dollar_object,
                input_formats,
                self.plugin_map)

        return output_content

    def save_loaded_to_disk(self):
        outputs = []
        for dollar_object_id, dollar_object in self.dollar_id_map.get_map().items():
            dollar_file = DollarFile(
                    dollar_object.get_path(),
                    dollar_object.get_content(),
                    "mdd")
            outputs.append(dollar_file)

        DollarFileWriter.clean_dir(self.conf_docs_path)
        DollarFileWriter.write_files(self.conf_docs_path, outputs)

    def get_dollar_id_map(self):
        return self.dollar_id_map
