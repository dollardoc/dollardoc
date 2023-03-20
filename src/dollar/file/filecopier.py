import os
import shutil


class FileCopier:

    @classmethod
    def copy_files(cls, path_from: str, path_to: str, file_ending: str):
        try:
            os.makedirs(path_to)
        except OSError:
            pass  # Allow path to exist

        dir_list = os.listdir(path_from)
        for item in dir_list:
            item_path_from = os.path.join(path_from, item)
            item_path_to = os.path.join(path_to, item)
            if os.path.isdir(item_path_from):
                cls.copy_files(item_path_from, item_path_to, file_ending)
            elif item.endswith(file_ending):
                shutil.copyfile(item_path_from, item_path_to)
