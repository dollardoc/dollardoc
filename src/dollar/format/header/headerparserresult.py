class HeaderParserResult:

    def __init__(self, header_object, header_end):
        self.header_object = header_object
        self.header_end = header_end

    def getheaderobject(self):
        return self.header_object

    def getheaderend(self):
        return self.header_end