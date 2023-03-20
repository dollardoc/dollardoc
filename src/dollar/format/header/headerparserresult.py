class HeaderParserResult:

    def __init__(self, header_object, header_end):
        self.header_object = header_object
        self.header_end = header_end

    def get_header_object(self):
        return self.header_object

    def get_header_end(self):
        return self.header_end
