from dollar.plugin.dollarplugin import DollarExtensionPlugin
from dollar.dollarobject import DollarObject


class PageExtensionPlugin(DollarExtensionPlugin):

    def extends(self):
        return None

    def getname(self):
        return "page"

    def getsecondaries(self):
        return []

    def getprimaries(self):
        return ["title", "description"]

    def validateprimaries(self, dollar_object: DollarObject):
        count = 0
        try:
            dollar_object.get("title")
        except:
            count = count + 1
        try:
            dollar_object.get("description")
        except:
            count = count + 1
        if count < 2:
            return "You need both \"title\" and \"description\" in your object"
        return None

    def execprimary(self, dollar_object: DollarObject):
        pass

    def execsecondary(self, dollar_object: DollarObject):
        pass
