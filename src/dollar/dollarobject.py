class DollarObject:

    def __init__(self, path, output_path, target_path):
        self.path = path
        self.output_path = output_path
        self.target_path = target_path
        self.header = {}
        self.backrefs = []
        self.backlinks = []

    def get_id(self):
        return self.get_header()["id"]

    def get_type(self):
        return self.get_header()["type"]

    def get_header(self):
        return self.header

    def get_backrefs(self):
        return self.backrefs

    def add_backref(self, backref_dollar_object):
        if backref_dollar_object not in self.backrefs:
            self.backrefs.append(backref_dollar_object)

    def get_backlinks(self):
        return self.backlinks

    def add_backlink(self, backlink_dollar_object):
        if backlink_dollar_object != self:
            if backlink_dollar_object not in self.backlinks:
                self.backlinks.append(backlink_dollar_object)

    def get_path(self):
        return self.path

    def get_output_path(self):
        return self.output_path

    def get_target_path(self):
        return self.target_path

    def __repr__(self):
        return "DollarObject(id: " + self.get_id() + ")"
