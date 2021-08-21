from ....localization.localization import Localizer
from ...presence_utilities import Utilities

def presence(rpc,client=None,data=None,content_data=None,config=None):
    _, mode_name = Utilities.fetch_mode_data(data,content_data)
    rpc.update(
        details=f"{Localizer.get_localized_text('presences','client_states','away')}",
        state=f"{mode_name}",
        large_image="game_icon_yellow",
        large_text="VALORANT",
    )
