import utils
import riot_api
import client_api 
import os

class Session:
    def __init__(self,client):
        self.config = utils.get_config()
        self.username = self.config['riot-account']['username']
        self.password = self.config['riot-account']['password']
        self.client = client
        self.uuid = None 
        self.match_id = None
        self.state = ""

    async def init_pregame(self,presence_data):
        self.uuid,headers = await client_api.get_auth(self.username,self.password)
        pregame_player = client_api.get_glz(f'/pregame/v1/players/{self.uuid}',headers)
        self.match_id = pregame_player['MatchID']
        self.state = "PREGAME"

    async def loop(self):
        uuid,headers = await client_api.get_auth(self.username,self.password)
        pregame_data = client_api.get_glz(f'/pregame/v1/matches/{self.match_id}',headers)
        print(pregame_data)




'''
        #agent select
        elif data["sessionLoopState"] == "PREGAME":
            game_map = utils.maps[data["matchMap"].split("/")[-1]]
            client.set_activity(
                state=party_state,
                details="Agent Select" + (f" - {queue_id}" if queue_id else ""),
                start = time if not time == False else None,
                large_image=f"splash_{game_map.lower()}",
                large_text=game_map,
                small_image=utils.mode_images[queue_id.lower()],
                party_id=data["partyId"],
                party_size=party_size,
            )

        #ingame
        elif data["sessionLoopState"] == "INGAME" and not data["provisioningFlow"] == "ShootingRange":
            game_map = utils.maps[data["matchMap"].split("/")[-1]]
            score = [data["partyOwnerMatchScoreAllyTeam"],data["partyOwnerMatchScoreEnemyTeam"]]
            client.set_activity(
                state=party_state,
                details=f"{queue_id.upper()}: {score[0]} - {score[1]}",
                start = time if not time == False else None,
                large_image=f"splash_{game_map.lower()}",
                large_text=game_map,
                small_image=utils.mode_images[queue_id.lower()],
                party_id=data["partyId"],
                party_size=party_size,
            )

        #ingame//range
        elif data["sessionLoopState"] == "INGAME" and data["provisioningFlow"] == "ShootingRange":
            game_map = utils.maps[data["matchMap"].split("/")[-1]]
            client.set_activity(
                state=party_state,
                details="THE RANGE",
                large_image=f"splash_{game_map.lower()}",
                large_text=game_map,
                small_image=utils.mode_images[queue_id.lower()],
                party_id=data["partyId"],
                party_size=party_size,
            )
>>>>>>> Stashed changes
'''