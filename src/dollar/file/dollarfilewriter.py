import os
import shutil

from dollar.confighandler import ConfigHandler
from dollar.dollarexecutionexception import DollarExecutionException


class DollarFileWriter:

    @staticmethod
    def write_files(outputs):
        target_path = ConfigHandler.get("target_path")
        try:
            shutil.rmtree(target_path)
        except:
            pass # Allow target to not exist
        for output in outputs:
            save_path = os.path.join(target_path, output.getpath())
            save_folder = os.path.split(save_path)[0]
            try:
                os.makedirs(save_folder)
            except OSError:
                # Allow save_folder to exist
                pass
            try:
                with open(save_path, "w") as f:
                    f.write(output.getcontent())
            except Exception as e:
                raise DollarExecutionException("Could not write file {}".format(save_path)) from e