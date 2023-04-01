from dollar.confighandler import ConfigHandler
from dollar.confighandler import ConfigType
from dollar.dollarcontext import DollarContext
from dollar.dollarobjectidmap import DollarObjectIdMap
from dollar.dollarobjectimpl import DollarObjectImpl
from dollar.dollarexception import DollarExecutionException
from dollar.dollarexception import DollarException
from dollar.file.dollarfile import DollarFile
from dollar.file.dollarfilereader import DollarFileReader
from dollar.file.dollarfilewriter import DollarFileWriter
from dollar.file.filecopier import FileCopier
from dollar.format.header.headerparser import HeaderParser
from dollar.format.raw.rawdollarparser import RawDollarParser
from dollar.format.transformer.headertransformer import HeaderTransformer
from dollar.format.transformer.inputtostrtransformer import InputToStrTransformer
from dollar.format.transformer.rawtoinputtransformer import RawToInputTransformer
from dollar.plugin.builtinpluginloader import BuiltinPluginLoader
from dollar.plugin.pluginhandler import PluginHandler


class DollarBuilder:

    @staticmethod
    def build():
        config_map = ConfigHandler.load_config_default()
        conf_docs_path = config_map.get(ConfigType.DOCS_PATH)
        conf_target_path = config_map.get(ConfigType.TARGET_PATH)
        conf_plugin_path = config_map.get(ConfigType.PLUGIN_PATH)
        conf_file_passthrough = config_map.get_str_list_opt(ConfigType.FILE_PASSTHROUGH)
        BuiltinPluginLoader.load(config_map)
        plugin_map = PluginHandler.import_plugins(conf_plugin_path, config_map)

        mdd_files = DollarFileReader.read_mdd_files(conf_docs_path)

        dollar_object_list = []

        dollar_id_map = DollarObjectIdMap()

        for mdd_file in mdd_files:
            path = mdd_file.get_path()
            content = mdd_file.get_content()

            dollar_object = DollarObjectImpl(
                    content,
                    path,
                    path[:-1],
                    "/" + path[:-1].replace("\\", "/"))

            dollar_context = DollarContext(path, 0, 0)

            header_parser_result = HeaderParser.parse(content, dollar_context)
            dollar_object.set_unparsed_header(header_parser_result.header_object)
            dollar_object.set_header_end(header_parser_result.header_end)

            try:
                dollar_id_map.add(dollar_object)
            except DollarException as e:
                raise DollarExecutionException(
                        e.get_message(),
                        dollar_context) from e
            dollar_object_list.append(dollar_object)

        for dollar_object in dollar_object_list:

            dollar_context = DollarContext(dollar_object.get_path(), 0, 0)

            dollar_object.set_header(
                    HeaderTransformer.transform(
                            dollar_object,
                            dollar_object.get_unparsed_header(),
                            dollar_context,
                            dollar_id_map))
            try:
                primary_plugin = plugin_map.get_extension(dollar_object.get_type())
            except DollarException as e:
                raise DollarExecutionException(
                        e.get_message(),
                        dollar_context) from e
            validate_plugin = primary_plugin
            visited = [dollar_object.get_type()]
            while True:
                if validate_plugin.extends() in visited:
                    raise DollarExecutionException(
                            "Extension plugin {} in Dollar Object {} was caught in a circular dependency loop"
                            .format(primary_plugin.get_name(), dollar_object.get_id()),
                            dollar_context)
                validation = validate_plugin.validate_primary(dollar_object)
                if validation is not None:
                    raise DollarExecutionException(
                            "Validation on {} failed: {}"
                            .format(dollar_object.get_id(), validation),
                            dollar_context)
                if validate_plugin.extends() is not None:
                    visited.append(validate_plugin.extends())
                    try:
                        validate_plugin = plugin_map.get_extension(validate_plugin.extends())
                    except DollarException as e:
                        raise DollarExecutionException(
                                e.get_message(),
                                dollar_context) from e
                else:
                    break

            primary_plugin.exec_primary(dollar_object)

            for key in dollar_object.get_header().keys():
                if plugin_map.has_extension_with_secondary_key(key):
                    plugin_map.get_extension_from_secondary_key(key)\
                            .exec_secondary(dollar_object)

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
                    InputToStrTransformer.transform_list(dollar_object, dollar_object.get_input_formats(), plugin_map))

        outputs = []
        for dollar_object in dollar_object_list:
            dollar_file = DollarFile(
                    dollar_object.get_output_path(),
                    dollar_object.get_output())
            outputs.append(dollar_file)
        DollarFileWriter.write_files(conf_target_path, outputs)

        for file_ending in conf_file_passthrough:
            FileCopier.copy_files(
                    conf_docs_path,
                    conf_target_path,
                    file_ending)
