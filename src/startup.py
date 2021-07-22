from InquirerPy.utils import color_print
import sys, psutil, time, cursor, valclient, ctypes, traceback, os

from .utilities.killable_thread import Thread
from .utilities.config.app_config import Config
from .utilities.config.modify_config import Config_Editor
from .utilities.processes import Processes
from .utilities.rcs import Riot_Client_Services
from .utilities.systray import Systray
from .utilities.version_checker import Checker
from .utilities.logging import Logger

from .presence.presence import Presence

from .webserver import server

# weird console window management stuff
kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()
kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x00|0x100)) #disable inputs to console
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7) #allow for ANSI sequences

class Startup:
    def __init__(self):
        cursor.hide()
        Config.check_config()
        Logger.create_logger()

        self.config = Config.fetch_config()
        Logger.debug(self.config)
        self.client = None
        if self.config["region"][0] == "": # try to autodetect region on first launch
            self.check_region() 
        ctypes.windll.kernel32.SetConsoleTitleW(f"valorant-rpc {self.config['version']}") 

        color_print([("Red", "waiting for rpc client")])
        try:
            self.presence = Presence()
            Startup.clear_line()
        except Exception as e:
            color_print([("Cyan",f"discord not detected! starting game without presence... ({e})")])
            if not Processes.are_processes_running():
                color_print([("Red", "starting VALORANT")])
                self.start_game()
                os._exit(1)

        self.run()


    def run(self):
        self.presence.update_presence("startup")
        Checker.check_version(self.config)
        if not Processes.are_processes_running():
            color_print([("Red", "starting VALORANT")])
            self.start_game()
        
        self.setup_client()

        self.systray = Systray(self.client,self.config)
        self.dispatch_systray()
        
        if self.client.fetch_presence() is None:
            self.wait_for_presence()

        self.dispatch_presence()
        self.dispatch_webserver() 
        
        color_print([("LimeGreen","program startup successful, hiding window in 5 seconds\n")])
        time.sleep(5)
        user32.ShowWindow(hWnd, 0) #hide window

        self.systray_thread.join()
        self.presence_thread.stop()
        color_print([("Red","presence closed")])
        

    def dispatch_webserver(self):
        server.client = self.client 
        server.config = self.config
        self.webserver_thread = Thread(target=server.start,daemon=True)
        self.webserver_thread.start()
        
    def dispatch_presence(self):
        self.presence_thread = Thread(target=self.presence.main_loop,daemon=True)
        self.presence_thread.start()

    def dispatch_systray(self):
        self.systray_thread = Thread(target=self.systray.run)
        self.systray_thread.start()

    def setup_client(self):
        self.client = valclient.Client(region=self.config["region"][0])
        self.client.activate()
        self.presence.client = self.client

    def wait_for_presence(self):
        presence_timeout = self.config["startup"]["presence_timeout"]
        presence_timer = 0 
        print()
        while self.client.fetch_presence() is None:
            Startup.clear_line()
            color_print([("Cyan", "["),("White",f"{presence_timer}"),("Cyan", "] waiting for presence... ")])
            presence_timer += 1
            if presence_timer >= presence_timeout:
                self.systray.exit()
                os._exit(1)
            time.sleep(1)
        Startup.clear_line()
        Startup.clear_line()

    def start_game(self):
        path = Riot_Client_Services.get_rcs_path()
        launch_timeout = self.config["startup"]["game_launch_timeout"]
        launch_timer = 0

        psutil.subprocess.Popen([path, "--launch-product=valorant", "--launch-patchline=live"])
        print()
        while not Processes.are_processes_running():
            Startup.clear_line()
            color_print([("Cyan", "["),("White",f"{launch_timer}"),("Cyan", "] waiting for valorant... ")])
            launch_timer += 1
            if launch_timer >= launch_timeout:
                self.systray.exit()
                os._exit(1)
            time.sleep(1)
        Startup.clear_line()

    def check_region(self):
        color_print([("Red bold",f"attempting to autodetect region")])
        client = valclient.Client(region="na")
        client.activate()
        sessions = client.riotclient_session_fetch_sessions()
        for _,session in sessions.items():
            if session["productId"] == "valorant":
                launch_args = session["launchConfiguration"]["arguments"]
                for arg in launch_args:
                    if "-ares-deployment" in arg:
                        region = arg.replace("-ares-deployment=","")
                        self.config["region"][0] = region
                        Config.modify_config(self.config)
                        color_print([("LimeGreen",f"autodetected region: {self.config['region'][0]}")])
                        time.sleep(5)
                        Systray.restart()

    @staticmethod
    def clear_line():
        sys.stdout.write("\033[F") # move cursor up one line
        sys.stdout.write("\r\033[K")