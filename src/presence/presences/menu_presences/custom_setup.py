from ...presence_utilities import Utilities
from ....localization.localization import Localizer

from .away import presence as away

def presence(rpc,client=None,data=None,content_data=None,config=None):
    is_afk = data["isIdle"]
    if is_afk:
        away(rpc,client,data,content_data,config)  
   
    else: 
        party_state,party_size = Utilities.build_party_state(data)
        data["MapID"] = data["matchMap"]
        game_map,map_name = Utilities.fetch_map_data(data,content_data)
        team = content_data["team_image_aliases"][data["customGameTeam"]] if data["customGameTeam"] in content_data["team_image_aliases"] else "game_icon_white"
        team_patched = content_data["team_aliases"][data["customGameTeam"]] if data["customGameTeam"] in content_data["team_aliases"].keys() else None
        team_patched = Utilities.localize_content_name(team_patched, "presences", "team_names", data["customGameTeam"])
        buttons = Utilities.get_join_state(client,config,data)

        rpc.update(
            state=party_state,
            details=Localizer.get_localized_text("presences","client_states","custom_setup"),
            large_image=f"splash_{game_map.lower()}",
            large_text=map_name,
            small_image=team,
            small_text=team_patched,
            party_size=party_size,
            party_id=data["partyId"],
            buttons=buttons
        )