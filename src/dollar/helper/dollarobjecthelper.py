from dollar.plugin.pluginmap import PluginMap
from dollar.dollarobject import DollarObject
from dollar.validationhelper import ValidationHelper

class DollarObjectHelper:

    @staticmethod
    def istype(dollar_object: DollarObject, dollar_object_type: str):
        if dollar_object.gettype() == dollar_object_type:
            return True
        dollar_object_type_temp = dollar_object_type
        while PluginMap.hasextension(dollar_object_type_temp):
            dollar_object_type_extends = PluginMap.getextension(dollar_object_type_temp).extends()
            if dollar_object_type == dollar_object_type_extends:
                return True
            dollar_object_type_temp = dollar_object_type_extends
        return False

    @staticmethod
    def gettitle(dollar_object: DollarObject):
        header = dollar_object.getheader()
        if "title" in header:
            title = header["title"]
            if ValidationHelper.validstr(title):
                return title
        return dollar_object.getid()