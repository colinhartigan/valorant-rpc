from .menu_presences import *

def presence(rpc,client=None,data=None,content_data=None):
    state_types = {
        "DEFAULT": default,
    }
    state_types[data['partyState']].presence(rpc,client=client,data=data,content_data=content_data)