import os
from typing import List

from dollar.dollarexception import DollarException
from dollar.file.dollarfile import DollarFile


class DollarFileReader:

    @classmethod
    def read_files(cls, src: str) -> List[DollarFile]:
        return cls._read_files(src)

    @classmethod
    def _read_files(cls, open_dir, _open_dir_start=None) -> List[DollarFile]:
        if _open_dir_start is None:
            _open_dir_start = open_dir
        result = []
        dir_list = os.listdir(open_dir)
        for item in dir_list:
            full_path = os.path.join(open_dir, item)
            if os.path.isdir(full_path):
                result2 = cls._read_files(full_path, _open_dir_start)
                result = result + result2
            else:
                try:
                    f = open(full_path, "r")
                except Exception as e:
                    raise DollarException("Failed to open file {}".format(full_path)) from e
                full_path_split = os.path.normpath(full_path).split(os.path.sep)
                open_dir_start_split = os.path.normpath(_open_dir_start).split(os.path.sep)
                to = len(full_path_split)
                if to > len(open_dir_start_split):
                    to = len(open_dir_start_split)
                new_path = str(os.path.sep).join(full_path_split[to:])
                try:
                    file_output = f.read()
                except Exception as e:
                    raise DollarException("Failed to read file {}".format(full_path)) from e
                result.append(DollarFile(new_path, file_output, item.split(".")[-1]))
                f.close()
        return result
