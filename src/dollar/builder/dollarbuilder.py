from dollar.confighandler import ConfigHandler
from dollar.confighandler import ConfigType
from dollar.dollarcontext import DollarContext
from dollar.dollarobjectidmap import DollarObjectIdMap
from dollar.file.dollarfile import DollarFile
from dollar.file.dollarfilereader import DollarFileReader
from dollar.file.dollarfilewriter import DollarFileWriter
from dollar.format.output.outputformatter import OutputFormatterMarkdown
from dollar.format.output.outputformatdollarobjectlinktype import OutputFormatDollarObjectLinkType
from dollar.format.raw.rawdollarparser import RawDollarParser
from dollar.format.transformer.inputtostrtransformer import InputToStrTransformer
from dollar.format.transformer.rawtoinputtransformer import RawToInputTransformer
from dollar.plugin.pluginhandler import PluginHandler
from dollar.helper.dollarobjectcreationhelper import DollarObjectCreationHelper


class DollarBuilder:

    @staticmethod
    def build():
        config_map = ConfigHandler.load_config_default()
        conf_docs_path = config_map.get(ConfigType.DOCS_PATH)
        conf_target_path = config_map.get(ConfigType.TARGET_PATH)
        conf_plugin_path = config_map.get(ConfigType.PLUGIN_PATH)
        conf_file_passthrough = config_map.get_str_list_opt(ConfigType.FILE_PASSTHROUGH)
        plugin_map = PluginHandler.import_plugins(conf_plugin_path, config_map)

        output_formatter = OutputFormatterMarkdown(OutputFormatDollarObjectLinkType.TO_MARKDOWN_FILE)

        files = DollarFileReader.read_files(conf_docs_path)
        mdd_files = [x for x in files if x.is_file_ending("mdd")]
        dollar_object_list = []

        dollar_id_map = DollarObjectIdMap()

        for mdd_file in mdd_files:
            path = mdd_file.get_path()
            content = mdd_file.get_content()
            dollar_object = DollarObjectCreationHelper.init(path, content, dollar_id_map)
            dollar_object_list.append(dollar_object)

        for dollar_object in dollar_object_list:
            DollarObjectCreationHelper.transform_header_primary(dollar_object, dollar_id_map, plugin_map)

        for dollar_object in dollar_object_list:
            DollarObjectCreationHelper.transform_header_secondary(dollar_object, dollar_id_map, plugin_map)

        for dollar_object in dollar_object_list:
            dollar_context_start = DollarContext(
                    dollar_object.get_path(),
                    dollar_object.get_header_end() + 2,
                    0)
            dollar_object.set_raw_formats(
                    RawDollarParser.parse(
                            dollar_object.get_content_without_header(),
                            dollar_context_start))

        for dollar_object in dollar_object_list:
            dollar_object.set_input_formats(
                    RawToInputTransformer.transform_list(
                            dollar_object,
                            dollar_object.get_raw_formats(),
                            dollar_id_map,
                            plugin_map))

        for dollar_object in dollar_object_list:
            dollar_object.set_output(
                    InputToStrTransformer.transform_list(
                            output_formatter,
                            dollar_object,
                            dollar_object.get_input_formats(),
                            plugin_map))

        outputs = []
        for dollar_object in dollar_object_list:
            dollar_file = DollarFile(
                    dollar_object.get_output_path(),
                    dollar_object.get_output(),
                    "md")
            outputs.append(dollar_file)

        conf_file_passthrough_lower = [file_ending.lower()[1:] for file_ending in conf_file_passthrough]
        other_files = [x for x in files if x.is_file_ending_in__assume_lower_case(conf_file_passthrough_lower)]
        outputs = outputs + other_files
        DollarFileWriter.clean_dir(conf_target_path)
        DollarFileWriter.write_files(conf_target_path, outputs)
