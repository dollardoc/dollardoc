from dollar.plugin.pluginmap import PluginMap
from dollar.dollarobject import DollarObject
from dollar.helper.validationhelper import ValidationHelper


class DollarObjectHelper:

    @staticmethod
    def is_type(dollar_object: DollarObject, dollar_object_type: str, plugin_map: PluginMap):
        if dollar_object.get_type() == dollar_object_type:
            return True
        dollar_object_type_temp = dollar_object.get_type()
        while plugin_map.has_extension(dollar_object_type_temp):
            dollar_object_type_extends = plugin_map.get_extension(dollar_object_type_temp).extends()
            if dollar_object_type == dollar_object_type_extends:
                return True
            dollar_object_type_temp = dollar_object_type_extends
        return False

    @staticmethod
    def get_title(dollar_object: DollarObject):
        header = dollar_object.get_header()
        if "title" in header:
            title = header["title"]
            if ValidationHelper.valid_str(title):
                return title
        return dollar_object.get_id()
