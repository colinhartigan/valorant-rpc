from ...presence_utilities import Utilities

from .away import presence as away

def presence(rpc,client=None,data=None,content_data=None,config=None):
    is_afk = data["isIdle"]
    if is_afk:
        away(rpc,client,data,content_data,config)  
   
    else: 
        party_state,party_size = Utilities.build_party_state(data)
        game_map = ""
        for gmap in content_data["maps"]:
            if gmap["path"] == data["matchMap"]:
                print(gmap)
                game_map = gmap["display_name"]
        rpc.update(
            state=party_state,
            details=f"Custom Game Setup",
            large_image=f"splash_{game_map.lower()}",
            large_text=game_map,
            small_image="game_icon",
            party_size=party_size,
            party_id=data["partyId"],
        )