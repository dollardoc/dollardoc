import os
import shutil
from typing import List

from dollar.dollarexception import DollarException
from dollar.file.dollarfile import DollarFile


class DollarFileWriter:

    @staticmethod
    def clean_dir(target_path):
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
    @staticmethod
    def write_files(target_path, outputs: List[DollarFile]):
        for output in outputs:
            save_path = os.path.join(target_path, output.get_path())
            save_folder = os.path.split(save_path)[0]
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            try:
                with open(save_path, "w") as f:
                    f.write(output.get_content())
            except Exception as e:
                raise DollarException("Could not write file {}".format(save_path)) from e
