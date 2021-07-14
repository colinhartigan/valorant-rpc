from PIL import Image
from pystray import Icon as icon, Menu as menu, MenuItem as item
import ctypes, os, urllib.request, sys

from .filepath import Filepath
from .config.modify_config import Config_Editor

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()

class Systray:

    def __init__(self):
        self.window_shown = True

    def run(self):
        Systray.generate_icon()
        systray_image = Image.open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'favicon.ico')))
        systray_menu = menu(
            item('config', Systray.modify_config),
            item('reload', Systray.restart),
            item('exit', self.exit)
        )
        self.systray = icon("valorant-rpc", systray_image, "valorant-rpc", systray_menu)
        self.systray.run()

    def exit(self):
        self.systray.visible = False
        self.systray.stop()
        try:
            os._exit(1)
        except:
            pass

    @staticmethod
    def generate_icon():
        urllib.request.urlretrieve('https://raw.githubusercontent.com/colinhartigan/valorant-rpc/v2/favicon.ico',Filepath.get_path(os.path.join(Filepath.get_appdata_folder(),'favicon.ico')))

    @staticmethod 
    def modify_config():
        Config_Editor()

    @staticmethod
    def restart():
        os.system('cls' if os.name == 'nt' else 'clear')
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 

    @staticmethod
    def tray_window_toggle(item):
        try:
            window_shown = not item.checked
            if window_shown:
                user32.ShowWindow(hWnd, 1)
            else:
                user32.ShowWindow(hWnd, 0)
        except:
            pass