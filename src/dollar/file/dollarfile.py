from typing import List

from dollar.dollarexception import DollarExecutionException
from dollar.dollarcontext import DollarContext
from dollar.helper.validationhelper import ValidationHelper


class DollarFile:

    def __init__(self, path, content, file_ending):
        if not ValidationHelper.valid_str(path):
            raise DollarExecutionException(
                    "Path passed to DollarFile must be valid string",
                    DollarContext(path, 0, 0))
        if not ValidationHelper.valid_str(content):
            content = ""
        if not ValidationHelper.valid_str(file_ending):
            raise DollarExecutionException(
                    "File Ending passed to DollarFile must be valid string",
                    DollarContext(path, 0, 0))
        self.path = path
        self.content = content
        self.file_ending = file_ending.lower()

    def get_path(self):
        return self.path

    def get_content(self):
        return self.content

    def get_file_ending(self):
        return self.file_ending

    def is_file_ending(self, file_ending_compare: str):
        return self.file_ending == file_ending_compare.lower()

    def is_file_ending_in(self, file_ending_compares: List[str]):
        file_ending_compares = [file_ending.lower() for file_ending in file_ending_compares]
        return self.file_ending in file_ending_compares

    def is_file_ending_in__assume_lower_case(self, file_ending_compares: List[str]):
        return self.file_ending in file_ending_compares
