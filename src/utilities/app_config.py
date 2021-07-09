import json
import os
from .filepath import Filepath

class Config:

    @staticmethod
    def fetch_config():
        try:
            with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'config.json'))) as f:
                config = json.load(f)
                return config
        except:
            return Config.create_blank_config()

    @staticmethod
    def modify_config(new_config):
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'config.json')), 'w') as f:
            json.dump(new_config, f)

        return Config.fetch_config()

    @staticmethod
    def create_blank_config():
        config = {
            "startup": {
                "game_launch_timeout": 80,
                "lockfile_timeout": 20,
                "presence_timeout": 20,
            }
        }
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'config.json')), 'w') as f:
            json.dump(config, f)
        return Config.fetch_config()
