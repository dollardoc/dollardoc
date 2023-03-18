class DollarObject:

    def __init__(self, path, output_path, target_path):
        self.path = path
        self.output_path = output_path
        self.target_path = target_path
        self.header = {}
        self.backrefs = []
        self.backlinks = []

    def getid(self):
        return self.getheader()["id"]

    def gettype(self):
        return self.getheader()["type"]

    def getheader(self):
        return self.header

    def getbackrefs(self):
        return self.backrefs

    def addbackref(self, backref_dollar_object):
        if backref_dollar_object not in self.backrefs:
            self.backrefs.append(backref_dollar_object)

    def getbacklinks(self):
        return self.backlinks

    def addbacklink(self, backlink_dollar_object):
        if backlink_dollar_object != self:
            if backlink_dollar_object not in self.backlinks:
                self.backlinks.append(backlink_dollar_object)

    def getpath(self):
        return self.path

    def getoutputpath(self):
        return self.output_path

    def gettargetpath(self):
        return self.target_path

    def __repr__(self):
        return "DollarObject(id: " + self.getid() + ")"
