from typing import Optional

from dollar.dollarobjectimpl import DollarObjectImpl
from dollar.dollarcontext import DollarContext
from dollar.dollarexception import DollarExecutionException
from dollar.dollarexception import DollarException
from dollar.format.header.headerparser import HeaderParser
from dollar.format.transformer.headertransformer import HeaderTransformer
from dollar.dollarobjectidmap import DollarObjectIdMap
from dollar.plugin.pluginmap import PluginMap


class DollarObjectCreationHelper:
    @staticmethod
    def init(path: str, content: str, dollar_id_map: Optional[DollarObjectIdMap]) -> DollarObjectImpl:
        dollar_object = DollarObjectImpl(
                content,
                path,
                path[:-1],
                "/" + path[:-1].replace("\\", "/"))

        dollar_context = DollarContext(path, 0, 0)

        header_parser_result = HeaderParser.parse(content, dollar_context)
        dollar_object.set_unparsed_header(header_parser_result.header_object)
        dollar_object.set_header_end(header_parser_result.header_end)

        if dollar_id_map is not None:
            try:
                dollar_id_map.add(dollar_object)
            except DollarException as e:
                raise DollarExecutionException(
                        e.get_message(),
                        dollar_context) from e
        return dollar_object

    @staticmethod
    def transform_header_primary(
            dollar_object: DollarObjectImpl,
            dollar_id_map: DollarObjectIdMap,
            plugin_map: PluginMap):
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

    @staticmethod
    def transform_header_secondary(
            dollar_object: DollarObjectImpl,
            dollar_id_map: DollarObjectIdMap,
            plugin_map: PluginMap):
        for key in dollar_object.get_header().keys():
            if plugin_map.has_extension_with_secondary_key(key):
                plugin_map.get_extension_from_secondary_key(key)\
                        .exec_secondary(dollar_object)  # TODO: Handle backrefs in dollar instead
