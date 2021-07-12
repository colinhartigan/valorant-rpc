from ...presence_utilities import Utilities

from .away import presence as away

def presence(rpc,client=None,data=None,content_data=None,config=None):
    is_afk = data["isIdle"]
    if is_afk:
        away(rpc,client,data,content_data,config)  
   
    else: 
        party_state,party_size = Utilities.build_party_state(data)
        game_map = Utilities.fetch_map_data(data,content_data)
        team = content_data["team_image_aliases"][data["customGameTeam"]] if data["customGameTeam"] in content_data["team_image_aliases"] else "game_icon_white"
        team_patched = content_data["team_aliases"][data["customGameTeam"]] if data["customGameTeam"] in content_data["team_aliases"].keys() else None
        
        rpc.update(
            state=party_state,
            details=f"Custom Game Setup",
            large_image=f"splash_{game_map.lower()}",
            large_text=game_map,
            small_image=team,
            small_text=team_patched,
            party_size=party_size,
            party_id=data["partyId"],
        )