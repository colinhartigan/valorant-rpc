from PIL import Image
from pystray import Icon as icon, Menu as menu, MenuItem as item
import ctypes, os

from .filepath import Filepath
from .config.modify_config import Config_Editor

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()
kernel32 = ctypes.windll.kernel32
#kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128) #disable inputs to console

class Systray:

    def __init__(self):
        self.window_shown = True

    def run(self):
        current_dir = os.path.dirname(__file__)
        favicon = Filepath.get_path(os.path.join(current_dir,'../../favicon.ico'))
        systray_image = Image.open(favicon)
        systray_menu = menu(
            item('config', Systray.modify_config),
            item('exit', self.exit)
        )
        self.systray = icon("valorant-rpc", systray_image, "valorant-rpc", systray_menu)
        self.systray.run() 


    def exit(self):
        self.systray.visible = False
        self.systray.stop()

    @staticmethod 
    def modify_config():
        Config_Editor()

    @staticmethod
    def tray_window_toggle(icon, item):
        try:
            window_shown = not item.checked
            if window_shown:
                user32.ShowWindow(hWnd, 1)
            else:
                user32.ShowWindow(hWnd, 0)
        except:
            pass