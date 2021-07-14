from pypresence import Presence as PyPresence
from pypresence.exceptions import InvalidPipe
from InquirerPy.utils import color_print
import time, sys, traceback, os, ctypes

from ..utilities.config.app_config import Config
from ..content.content_loader import Loader
from .presences import (ingame,menu,startup,pregame)

kernel32 = ctypes.WinDLL('kernel32')

class Presence:

    def __init__(self):
        self.config = Config.fetch_config()
        self.client = None
        try:
            self.rpc = PyPresence(client_id=str(self.config["client_id"]))
            self.rpc.connect()
        except InvalidPipe as e:
            raise Exception(e)
        self.content_data = {}
    
    def main_loop(self):
        try:
            self.content_data = Loader.load_all_content(self.client)
            color_print([("LimeGreen bold", "presence running!")])
            while True:
                presence_data = self.client.fetch_presence()
                if presence_data is not None:
                    self.update_presence(presence_data["sessionLoopState"],presence_data)
                    #print(presence_data)
                    time.sleep(self.config["presence_refresh_interval"])
                else:
                    os._exit(1)

                    
        except Exception as e:
            color_print([("Red bold","the program encountered an error: please create an issue with the traceback below if this problem persists")])
            color_print([("Red","traceback:")])
            traceback.print_exc()
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x40|0x100))
            input("press enter to continue...")
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