import json
import os
from ..filepath import Filepath

default_config = {
    "version": "v3.0",
    "region": "na",
    "client_id": 811469787657928704,
    "presence_refresh_interval": 5,
    "presences": {
        "menu": {
            "show_rank_in_comp_lobby": False
        },
        "modes": {
            "competitive": {
                "show_rank_instead_of_agent": False,
            }
        }
    },
    "startup": {
        "game_launch_timeout": 30,
        "presence_timeout": 60,
    },
}

class Config:

    @staticmethod
    def fetch_config():
        try:
            with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'config.json'))) as f:
                config = json.load(f)
                return config
        except:
            return Config.create_default_config()

    @staticmethod
    def modify_config(new_config):
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'config.json')), 'w') as f:
            json.dump(new_config, f)

        return Config.fetch_config()

    @staticmethod
    def check_config():
        # ???????
        # my brain hurts
        # i bet theres a way better way to write this but im just braindead
        config = Config.fetch_config()
        
        def check_for_new_vars(blank,current):
            for key,value in blank.items():
                if not key in current.keys():
                    current[key] = value
                if key == "version": 
                    current[key] = value
                if isinstance(value,dict):
                    check_for_new_vars(value,current[key])
            
        def remove_unused_vars(blank,current):
            def check(bl,cur):
                for key,value in list(cur.items()):
                    if not key in bl.keys():
                        del cur[key]
                    if isinstance(value,dict) and key in list(cur.keys()):
                        check(bl[key],value)

            check(blank,current)
            return current

        check_for_new_vars(default_config,config)
        config = remove_unused_vars(default_config,config)
        Config.modify_config(config)

    @staticmethod
    def create_default_config():
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'config.json')), 'w') as f:
            json.dump(default_config, f)
        return Config.fetch_config()