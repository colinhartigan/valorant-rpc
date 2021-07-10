import os, json

class Riot_Client_Services:

    @staticmethod 
    def get_rcs_path():
        riot_installs_path = os.path.expandvars("%PROGRAMDATA%\\Riot Games\\RiotClientInstalls.json")
        try:
            with open(riot_installs_path, "r") as file:
                client_installs = json.load(file)
                rcs_path = os.path.abspath(client_installs["rc_default"])
                if not os.access(rcs_path, os.X_OK):
                    return None
                return rcs_path
        except FileNotFoundError:
            return None
    