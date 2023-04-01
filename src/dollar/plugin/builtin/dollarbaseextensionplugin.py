from dollar.plugin.dollarplugin import DollarExtensionPlugin
from dollar.dollarobject import DollarObject


class DollarBaseExtensionPlugin(DollarExtensionPlugin):

    def extends(self):
        return None

    def get_name(self):
        return "dollar"

    def get_secondaries(self):
        return []

    def get_primaries(self):
        return ["id", "type"]

    def validate_primary(self, dollar_object: DollarObject):
        count = 2
        ret = ""

        if "id" not in dollar_object.get_header():
            count = count - 1
            ret = "Type dollar requires \"id\" key"
        if "type" not in dollar_object.get_header():
            count = count - 1
            ret = "Type dollar requires \"type\" key"

        if count == 0:
            return "Type dollar requires \"id\" and \"type\" keys"
        elif count == 1:
            return ret

        return None

    def exec_primary(self, dollar_object: DollarObject):
        pass

    def exec_secondary(self, dollar_object: DollarObject):
        pass
