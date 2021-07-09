from InquirerPy.utils import color_print
import sys, psutil, time

from .utilities.app_config import Config
from .utilities.processes import Processes
from .utilities.rcs import Riot_Client_Services

class Startup:
    '''
    startup procedure: 
    check if valorant running, if not start it
    load config/check region
    build valclient client
    dispatch presence loop to a separate thread so can listen for config command
    '''
    def __init__(self):
        self.config = Config.fetch_config()
        self.run()


    def run(self):

        if not Startup.check_processes():
            color_print([("Red", "VALORANT not detected, starting game")])
            self.start_game()

        

    def start_game(self):
        path = Riot_Client_Services.get_rcs_path()
        launch_timeout = self.config["startup"]["game_launch_timeout"]
        launch_timer = 0

        psutil.subprocess.Popen([path, "--launch-product=valorant", "--launch-patchline=live"])
        while not Startup.check_processes():
            sys.stdout.write("\033[F") # move cursor up one line
            color_print([("Cyan", "["),("White",f"{launch_timer}"),("Cyan", "] waiting for valorant... ")])
            launch_timer += 1
            if launch_timer >= launch_timeout:
                sys.exit()
            time.sleep(1)

    @staticmethod
    def check_processes():
        if Processes.are_processes_running():
            return True 
        else:
            return False