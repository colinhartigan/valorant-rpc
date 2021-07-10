from .menu_presences import (default,queue,custom_setup)

def presence(rpc,client=None,data=None,content_data=None,config=None):
    state_types = {
        "DEFAULT": default,
        "MATCHMAKING": queue,
        "CUSTOM_GAME_SETUP": custom_setup,
    }
    if data['partyState'] in state_types.keys():
        state_types[data['partyState']].presence(rpc,client=client,data=data,content_data=content_data,config=config)