from ....localization.localization import Localizer
from ...presence_utilities import Utilities

def presence(rpc,client=None,data=None,content_data=None,config=None):
    _, mode_name = Utilities.fetch_mode_data(data,content_data)
    
    party_state,party_size = Utilities.build_party_state(data)
    if data["queueId"] == "competitive" and Localizer.get_config_value("presences","menu","show_rank_in_comp_lobby"): 
        small_image, small_text = Utilities.fetch_rank_data(client,content_data)
    
    rpc.update(
        details=f"{Localizer.get_localized_text('presences','client_states','menu')} - {mode_name}",
        state=f"{Localizer.get_localized_text('presences','client_states','away')} (" + party_state + ")",
        large_image="game_icon_yellow",
        large_text=f"{Localizer.get_localized_text('presences','leveling','level')} {data['accountLevel']}",
        small_image=small_image,
        small_text=small_text,
    )
    
