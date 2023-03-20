from dollar.dollarexception import DollarExecutionException
from dollar.dollarcontext import DollarContext
from dollar.helper.validationhelper import ValidationHelper


class DollarFile:

    def __init__(self, path, content):
        if not ValidationHelper.valid_str(path):
            raise DollarExecutionException(
                    "Path passed to DollarFile must be valid string",
                    DollarContext(path, 0, 0))
        if not ValidationHelper.valid_str(content):
            raise DollarExecutionException(
                    "Content passed to DollarFile must be valid string",
                    DollarContext(path, 0, 0))
        self.path = path
        self.content = content

    def get_path(self):
        return self.path

    def get_content(self):
        return self.content
