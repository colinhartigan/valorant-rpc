from InquirerPy import inquirer
from .locales import Locales

class Localizer:

    locale = "en-us"
    config = None

    @staticmethod
    def get_localized_text(section,key):
        localized = Locales[Localizer.locale].get(key)
        if localized is not None:
            return Locales[Localizer.locale][section][key]
        return Locales["en-us"][section][key]

    @staticmethod
    def get_config_key(key):
        for k,value in Locales[Localizer.locale]["config"].items():
            #print(f"{k}/{value}")
            if k == key:
                return value
        return key

    @staticmethod
    def unlocalize_key(key):
        for k,value in Locales[Localizer.locale]["config"].items():
            #print(f"{k}/{value}")
            if value == key:
                return k
        return key

    def get_config_value(*keys):
        localized_keys = [Localizer.get_config_key(key) for key in keys]
        result = Localizer.config
        for key in localized_keys:
            result = result[key]
        return result

    @staticmethod
    def set_locale(config):
        Localizer.locale = config["locale"][0]

    @staticmethod
    def prompt_locale(config):
        locale = config["locale"]
        current = locale[0]
        options = locale[1]
        choice = inquirer.select(
            message=f"select your locale (language)",
            default=current,
            choices={option:option for option in options},
            pointer=">"
        )
        choice = choice.execute()
        locale[0] = choice 
        return config