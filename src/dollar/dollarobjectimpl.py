import yaml

from dollar.dollarobject import DollarObject





class DollarObjectImpl(DollarObject):

    def __init__(self, content, path, output_path, target_path):
        self.content = content.split("\n")
        self.path = path
        self.output_path = output_path
        self.target_path = target_path
        self.header_end = 0
        self.header = None
        self.unparsed_header = {}
        self.backrefs = []
        self.backlinks = []
        self.raw_formats = []
        self.input_formats = []
        self.output = ""

    def getid(self):
        if self.header is None:
            return self.unparsed_header["id"]
        return self.header["id"]

    def gettype(self):
        if self.header is None:
            return self.unparsed_header["type"]
        return self.header["type"]

    def getheader(self):
        return self.header

    def setheader(self, header):
        self.header = header

    def getheaderend(self):
        return self.header_end

    def setheaderend(self, header_end):
        self.header_end = header_end

    def getunparsedheader(self):
        return self.unparsed_header

    def setunparsedheader(self, unparsed_header):
        self.unparsed_header = unparsed_header

    def getcontentwithoutheader(self):
        return "\n".join(self.content[self.header_end + 1:])

    def getoutput(self) -> str:
        return self.output

    def setoutput(self, output: str):
        self.output = output

    def getpath(self):
        return self.path

    def getoutputpath(self):
        return self.output_path

    def gettargetpath(self):
        return self.target_path

    def getrawformats(self):
        return self.raw_formats

    def setrawformats(self, raw_formats):
        self.raw_formats = raw_formats

    def getinputformats(self):
        return self.input_formats

    def setinputformats(self, input_formats):
        self.input_formats = input_formats
