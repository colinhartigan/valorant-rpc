from InquirerPy.utils import color_print
import sys, psutil, time, cursor, valclient

from .utilities.killable_thread import Thread
from .utilities.config.app_config import Config
from .utilities.processes import Processes
from .utilities.rcs import Riot_Client_Services
from .utilities.systray import Systray

from .presence.presence import Presence

class Startup:
    def __init__(self):
        cursor.hide()
        Config.check_config()

        self.config = Config.fetch_config()
        self.systray = Systray()
        self.client = None
        color_print([("Red", "waiting for rpc client")])
        self.presence = Presence()

        self.dispatch_systray()
        self.run()


    def run(self):
        self.presence.update_presence("startup")
        if not Processes.are_processes_running():
            color_print([("Red", "starting VALORANT")])
            self.start_game()
        
        self.setup_client()
        
        if self.client.fetch_presence() is None:
            self.wait_for_presence()

        self.dispatch_presence()
        self.systray_thread.join()
        self.presence_thread.stop()
        color_print([("Red","presence closed")])
        
        
        
    def dispatch_presence(self):
        self.presence_thread = Thread(target=self.presence.main_loop,daemon=True)
        self.presence_thread.start()

    def dispatch_systray(self):
        self.systray_thread = Thread(target=self.systray.run,daemon=True)
        self.systray_thread.start()

    def setup_client(self):
        self.client = valclient.Client(region=self.config["region"])
        self.client.hook()
        self.presence.client = self.client

    def wait_for_presence(self):
        presence_timeout = self.config["startup"]["presence_timeout"]
        presence_timer = 0 

        while self.client.fetch_presence() is None:
            sys.stdout.write("\033[F") # move cursor up one line
            color_print([("Cyan", "["),("White",f"{presence_timer}"),("Cyan", "] waiting for presence... ")])
            presence_timer += 1
            if presence_timer >= presence_timeout:
                sys.exit()
            time.sleep(1)

    def start_game(self):
        path = Riot_Client_Services.get_rcs_path()
        launch_timeout = self.config["startup"]["game_launch_timeout"]
        launch_timer = 0

        psutil.subprocess.Popen([path, "--launch-product=valorant", "--launch-patchline=live"])
        while not Processes.are_processes_running():
            sys.stdout.write("\033[F") # move cursor up one line
            color_print([("Cyan", "["),("White",f"{launch_timer}"),("Cyan", "] waiting for valorant... ")])
            launch_timer += 1
            if launch_timer >= launch_timeout:
                sys.exit()
            time.sleep(1)