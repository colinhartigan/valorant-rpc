from InquirerPy.utils import color_print
from InquirerPy import inquirer
from valclient.client import Client

from .app_config import Config, default_config


class Config_Editor:

    # my friends made me listen to alvin and the chipmunks music
    # while writing this so i apologize for how poorly its written

    def __init__(self):
        self.config = Config.fetch_config()

        self.config_menu("main", self.config)

    def config_menu(self, section, choices, callback=None, callback_args=None):
        # recursion makes me want to die but its for a good cause

        prompt_choices = [
            {"name": f"{setting}" + (f" ({value})" if not isinstance(value, dict) else " (>>)"), "value": setting} for
            setting, value in choices.items()
        ]
        prompt_choices.insert(0, {"name": "back", "value": "back"})

        choice = inquirer.select(
            message=f"[{section}] select a configuration option",
            choices=prompt_choices,
            pointer=">"
        )
        choice = choice.execute()

        if choice == "back":
            if section != "main":
                callback(*callback_args)
            elif callback is None:
                Config.modify_config(self.config)
                color_print(
                    [("LimeGreen", "config saved! restart the program if you changed your region.")])
                return
        else:
            if isinstance(choices[choice], dict):
                self.config_menu(choice, choices[choice], callback=self.config_menu,
                                 callback_args=(section, choices, callback, callback_args))
            else:
                choices[choice] = self.config_set(choice, choices[choice])
                self.config_menu(section, choices, callback, callback_args)

    @staticmethod
    def config_set(name, option):
        if name == "region":
            return Config_Editor.set_region(option)

        if type(option) is str:
            choice = inquirer.text(
                message=f"set value for {name} (expecting str)",
                default=str(option),
                validate=lambda result: not result.isdigit(),
                filter=lambda result: str(result)
            )
            choice = choice.execute()
            return choice

        if type(option) is int:
            choice = inquirer.text(
                message=f"set value for {name} (expecting int)",
                default=str(option),
                validate=lambda result: result.isdigit(),
                filter=lambda result: int(result)
            )
            choice = choice.execute()
            return choice

        if type(option) is bool:
            choice = inquirer.select(
                message=f"set value for {name}",
                default=option,
                choices=[{"name": "true", "value": True},
                         {"name": "false", "value": False}],
                pointer=">"
            )
            choice = choice.execute()
            return choice

    @staticmethod
    def set_region(option):
        regions = Client.fetch_regions()
        choice = inquirer.select(
            message="select your region",
            choices=[{"name": region, "value": region} for region in regions],
            default=option,
            pointer=">"
        )
        choice = choice.execute()
        return choice