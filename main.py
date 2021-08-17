from InquirerPy.utils import color_print
import ctypes,os,traceback

from src.startup import Startup 
from src.utilities.config.app_config import default_config
from src.localization.localization import Localizer

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()

if __name__ == "__main__":
    color_print([("Tomato",f""" _   _____   __   ____  ___  ___   _  ________                
| | / / _ | / /  / __ \/ _ \/ _ | / |/ /_  __/__________  ____
| |/ / __ |/ /__/ /_/ / , _/ __ |/    / / / /___/ __/ _ \/ __/
|___/_/ |_/____/\____/_/|_/_/ |_/_/|_/ /_/     /_/ / .__/\__/ 
                                                  /_/ """),("White",f"{default_config['version']}\n")])
    try:
        app = Startup()
    except:
        user32.ShowWindow(hWnd, 1)
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x40|0x100))
        color_print([("Red bold",Localizer.get_localized_text("prints","errors","error_message"))])
        traceback.print_exc()
        input(Localizer.get_localized_text("prints","errors","exit"))
        os._exit(1)