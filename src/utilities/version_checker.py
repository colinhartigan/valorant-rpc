import requests 
from InquirerPy.utils import color_print

from ..localization.localization import Localizer

class Checker:
    @staticmethod 
    def check_version(config):
        try:
            current_version = Localizer.get_config_value("version")
            data = requests.get("https://api.github.com/repos/colinhartigan/valorant-rpc/releases/latest")
            latest = data.json()["tag_name"]
            if latest != current_version:
                color_print([("Yellow bold",f"({current_version} -> {latest}) {Localizer.get_localized_text('prints','version_checker','update_available')} "),("Cyan underline",f"https://github.com/colinhartigan/valorant-rpc/releases/tag/{latest}")])
        except:
            color_print([("Yellow bold",Localizer.get_localized_text("prints","version_checker","checker_error"))])
