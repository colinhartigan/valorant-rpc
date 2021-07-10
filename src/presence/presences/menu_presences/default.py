from ...presence_utilities import Utilities

def presence(rpc,client=None,data=None,content_data=None):
    is_afk = False #data["isIdle"]
    party_state,party_size = Utilities.build_party_state(data)
    
    if is_afk:
        pass 
    
    else:
        rpc.update(
            state=party_state,
            details=f"Menu - {content_data['queue_aliases'][data['queueId']]}",
            large_image="game_icon",
            large_text=f"Level {data['accountLevel']}",
            small_image=f"mode_{data['queueId'] if data['queueId'] in content_data['modes_with_icons'] else 'unrated'}",
            party_size=party_size,
            party_id=data["partyId"],
        )