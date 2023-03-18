from dollar.dollarexecutionexception import DollarExecutionException
from dollar.validationhelper import ValidationHelper


class DollarFile:

    def __init__(self, path, content):
        if not ValidationHelper.validstr(path):
            raise DollarExecutionException("Path passed to DollarFile must be valid string")
        if not ValidationHelper.validstr(content):
            raise DollarExecutionException("Content passed to DollarFile must be valid string")
        self.path = path
        self.content = content

    def getpath(self):
        return self.path

    def getcontent(self):
        return self.content
