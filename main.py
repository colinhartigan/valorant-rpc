from src.startup import Startup 
from InquirerPy.utils import color_print

from src.utilities.config.app_config import default_config

if __name__ == "__main__":
    color_print([("Tomato",f""" _   _____   __   ____  ___  ___   _  ________                
| | / / _ | / /  / __ \/ _ \/ _ | / |/ /_  __/__________  ____
| |/ / __ |/ /__/ /_/ / , _/ __ |/    / / / /___/ __/ _ \/ __/
|___/_/ |_/____/\____/_/|_/_/ |_/_/|_/ /_/     /_/ / .__/\__/ 
                                                  /_/ """),("White",f"{default_config['version']}\n")])
    app = Startup()