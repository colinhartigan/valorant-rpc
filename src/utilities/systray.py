from PIL import Image
from pystray import Icon as icon, Menu as menu, MenuItem as item
import ctypes, os, urllib.request, sys, time, pyperclip
from InquirerPy.utils import color_print

from .filepath import Filepath
from .config.modify_config import Config_Editor
from ..localization.localization import Localizer
from ..presence.presence_utilities import Utilities

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()

window_shown = False


class Systray:

    def __init__(self, client, config):
        self.client = client
        self.config = config

    def run(self):
        global window_shown
        Systray.generate_icon()
        systray_image = Image.open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'favicon.ico')))
        systray_menu = menu(
            item('show window', Systray.tray_window_toggle, checked=lambda item: window_shown),
            item('config', Systray.modify_config),
            #item('copy join link', self.copy_join_link),
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

    def copy_join_link(self):
        pyperclip.copy(Utilities.get_join_state(self.client,self.config)[0]["url"])

    @staticmethod
    def generate_icon():
        urllib.request.urlretrieve('https://raw.githubusercontent.com/colinhartigan/valorant-rpc/v2/favicon.ico',Filepath.get_path(os.path.join(Filepath.get_appdata_folder(),'favicon.ico')))

    @staticmethod 
    def modify_config():
        user32.ShowWindow(hWnd, 1)
        Config_Editor()
        if not window_shown:
            color_print([("LimeGreen",f"{Localizer.get_localized_text('prints','systray','hiding_window')}\n")])
            time.sleep(1)
            user32.ShowWindow(hWnd, 0)

    @staticmethod
    def restart():
        user32.ShowWindow(hWnd, 1)
        os.system('cls' if os.name == 'nt' else 'clear')
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 

    @staticmethod
    def tray_window_toggle(icon,item):
        global window_shown
        try:
            window_shown = not item.checked
            if window_shown:
                user32.ShowWindow(hWnd, 1)
            else:
                user32.ShowWindow(hWnd, 0)
        except Exception as e:
            pass # oh no! bad python practices! 