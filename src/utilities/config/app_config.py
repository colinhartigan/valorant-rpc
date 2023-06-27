import json, os
from valclient.client import Client 

from ..filepath import Filepath

from ...localization.locales import Locales
from ...localization.localization import Localizer

default_config = {
    "version": "v3.2.3",
    "region": ["",Client.fetch_regions()],
    "client_id": 811469787657928704,
    "presence_refresh_interval": 3,
    "locale": ["",[locale for locale,data in Locales.items() if data != {}]],
    "presences": {
        "menu": {
            "show_rank_in_comp_lobby": True,
            #"show_join_button_with_open_party": True,
            #"allow_join_requests": False,
        },
        "modes": {
            "all": {
                "small_image": ["agent",["rank","agent","map"]],
                "large_image": ["map",["rank","agent","map"]],
            },
            "range": {
                "show_rank_in_range": False,
            }
        }
    },
    "startup": {
        "game_launch_timeout": 50,
        "presence_timeout": 60,
        "show_github_link": True,
        "auto_launch_skincli": True,
    },
}

class Config:

    @staticmethod
    def fetch_config():
        try:
            with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "config.json"))) as f:
                config = json.load(f)
                return config
        except:
            return Config.create_default_config()

    @staticmethod
    def modify_config(new_config):
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "config.json")), "w") as f:
            json.dump(new_config, f)

        return Config.fetch_config()

    @staticmethod
    def check_config():
        # ???????
        # my brain hurts
        # i bet theres a way better way to write this but im just braindead
        config = Config.fetch_config()
        unlocalized_config = Config.localize_config(config,True)
        
        def check_for_new_vars(blank,current):
            for key,value in blank.items():
                if not key in current.keys():
                    current[key] = value
                if type(value) != type(current[key]):
                    # if type of option is changed
                    current[key] = value
                if key == "version": 
                    # version can't be changed by the user lmao
                    current[key] = value
                if key == "region": 
                    current[key][1] = Client.fetch_regions() # update regions jic ya know
                if isinstance(value,list):
                    current[key][0] = current[key][0]
                    current[key][1] = blank[key][1]
                    if not current[key][0] in blank[key][1]:
                        current[key][0] = blank[key][0]
                if isinstance(value,dict):
                    check_for_new_vars(value,current[key])
            return current
            
        def remove_unused_vars(blank,current):
            def check(bl,cur):
                for key,value in list(cur.items()):
                    if not key in bl.keys():
                        del cur[key]
                    if isinstance(value,dict) and key in list(cur.keys()):
                        check(bl[key],value)

            check(blank,current)
            return current

        unlocalized_config = check_for_new_vars(default_config,unlocalized_config)
        unlocalized_config = remove_unused_vars(default_config,unlocalized_config)
        config = Config.localize_config(unlocalized_config)
        Config.modify_config(config)
        return config


    @staticmethod
    def localize_config(config,unlocalize=False):
        def check(blank,current):
            for key,value in list(blank.items() if not unlocalize else current.items()):
                new_key = Localizer.get_config_key(key) if not unlocalize else Localizer.unlocalize_key(key)
                if new_key != key:
                    if unlocalize:
                        current[new_key] = current[key]
                        del current[key]
                    else:
                        #print(current[key])
                        current[new_key] = current[key]
                        del current[key]

                if isinstance(value,list):
                    if not unlocalize:
                        new_options = [Localizer.get_config_key(x) for x in value[1]]
                        current[new_key][0] = Localizer.get_config_key(current[new_key][0])
                        current[new_key][1] = new_options

                    else:
                        new_options = [Localizer.unlocalize_key(x) for x in value[1]]
                        unlocalized = Localizer.unlocalize_key(current[new_key][0])
                        value[0] = unlocalized
                        value[1] = new_options
                
                if isinstance(value,dict):
                    check(value,current[new_key])

        check(default_config,config)
        return config

    @staticmethod
    def create_default_config():
        if not os.path.exists(Filepath.get_appdata_folder()):
            os.mkdir(Filepath.get_appdata_folder())
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "config.json")), "w") as f:
            json.dump(default_config, f)
        return Config.fetch_config()
