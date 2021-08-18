import os, sys, json
from InquirerPy.utils import color_print

class Program_Data:

    installs_path = os.path.expandvars("%PROGRAMDATA%\\valorant-tools\\installs.json")

    @staticmethod
    def update_file_location():
        if getattr(sys, 'frozen', False):
            path = sys.executable
        else:
            color_print([("Yellow","running in a testing environment, cannot update installation path")])
            path = None

        if path is not None:
            installs = Program_Data.fetch_installs()
            installs["valorant-rpc"] = path
            Program_Data.modify_isntalls(installs)


    @staticmethod
    def fetch_installs():
        try:
            with open(Program_Data.installs_path) as f:
                installs = json.load(f)
                return installs
        except:
            return Program_Data.create_installs_file()

    @staticmethod
    def modify_isntalls(payload):
        with open(Program_Data.installs_path, "w") as f:
            json.dump(payload, f)

        return Program_Data.fetch_installs()

    @staticmethod
    def create_installs_file():
        Program_Data.check_for_folder()
        with open(Program_Data.installs_path, "w") as f:
            payload = {}
            json.dump(payload, f)

        return Program_Data.fetch_installs()

    @staticmethod
    def check_for_folder():
        if not os.path.isdir(Program_Data.installs_path):
            os.makedirs(Program_Data.installs_path)