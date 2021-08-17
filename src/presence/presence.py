from pypresence import Presence as PyPresence
from pypresence.exceptions import InvalidPipe
from InquirerPy.utils import color_print
import time, sys, traceback, os, ctypes

from ..utilities.config.app_config import Config
from ..content.content_loader import Loader
from ..localization.localization import Localizer
from .presences import (ingame,menu,startup,pregame)

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()

class Presence:

    def __init__(self):
        self.config = Config.fetch_config()
        self.client = None
        try:
            self.rpc = PyPresence(client_id=str(Localizer.get_config_value("client_id")))
            self.rpc.connect()
        except InvalidPipe as e:
            raise Exception(e)
        self.content_data = {}
    
    def main_loop(self):
        try:
            self.content_data = Loader.load_all_content(self.client)
            color_print([("LimeGreen bold", Localizer.get_localized_text("prints","presence","presence_running"))])
            while True:
                presence_data = self.client.fetch_presence()
                if presence_data is not None:
                    self.update_presence(presence_data["sessionLoopState"],presence_data)
                    #print(presence_data)
                    time.sleep(Localizer.get_config_value("presence_refresh_interval"))
                else:
                    os._exit(1)

                    
        except Exception as e:
            user32.ShowWindow(hWnd, 1)
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x40|0x100))
            color_print([("Red bold",Localizer.get_localized_text("prints","errors","error_message"))])
            traceback.print_exc()
            input(Localizer.get_localized_text("prints","errors","exit"))
            os._exit(1)

    def update_presence(self,ptype,data=None):
        presence_types = {
            "startup": startup,
            "MENUS": menu,
            "PREGAME": pregame,
            "INGAME": ingame,
        }
        if ptype in presence_types.keys():
            presence_types[ptype].presence(self.rpc,client=self.client,data=data,content_data=self.content_data,config=self.config)