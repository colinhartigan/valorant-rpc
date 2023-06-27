from ....localization.localization import Localizer
from ...presence_utilities import Utilities

def presence(rpc,client=None,data=None,content_data=None,config=None):    
    party_state,party_size = Utilities.build_party_state(data)
    small_image, mode_name = Utilities.fetch_mode_data(data,content_data)
    buttons = Utilities.get_join_state(client,config,data)
    small_text = mode_name

    if data["queueId"] == "competitive" and Localizer.get_config_value("presences","menu","show_rank_in_comp_lobby"): 
        small_image, small_text = Utilities.fetch_rank_data(client,content_data)

    

    rpc.update(
        state=party_state,
        details=f"{Localizer.get_localized_text('presences','client_states','away')} - {mode_name}",
        large_image="game_icon_yellow",
        large_text=f"{Localizer.get_localized_text('presences','leveling','level')} {data['accountLevel']}",
        small_image=small_image,
        small_text=small_text,
        party_size=party_size,
        party_id=data["partyId"],
        buttons=buttons
    )
