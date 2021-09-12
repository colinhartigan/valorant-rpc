from .ingame_presences.session import Game_Session
from .ingame_presences.range import Range_Session

def presence(rpc,client=None,data=None,content_data=None,config=None):
    coregame = client.coregame_fetch_player()

    if coregame is not None:
        match_id = coregame["MatchID"]
        if data["provisioningFlow"] != "ShootingRange":
            try:
                session = Game_Session(rpc,client,data,match_id,content_data,config)
                session.main_loop()
            except:
                pass
        else:
            session = Range_Session(rpc,client,data,match_id,content_data,config)
            session.main_loop()


