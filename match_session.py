import utils
import riot_api
import client_api 
import os
import asyncio

class Session:
    def __init__(self,client):
        self.loop = asyncio.get_event_loop()
        self.config = utils.get_config()
        self.username = self.config['riot-account']['username']
        self.password = self.config['riot-account']['password']
        self.client = client
        self.uuid = None 
        self.match_id = None
        self.agent_name = ""
        self.map = ""
        self.state = ""
        self.mode = ""
        

    def init_pregame(self,presence_data):
        self.uuid,headers = client_api.get_auth(self.username,self.password)
        pregame_player = client_api.get_glz(f'/pregame/v1/players/{self.uuid}',headers)
        self.match_id = pregame_player['MatchID']
        self.state = "PREGAME"
        self.map = utils.maps[presence_data["matchMap"].split("/")[-1]]
        self.mode = presence_data['queue_id']

    def pregame_loop(self,presence_data):
        uuid,headers = client_api.get_auth(self.username,self.password)
        pregame_data = client_api.get_glz(f'/pregame/v1/matches/{self.match_id}',headers)
        for team in pregame_data['Teams']:
            for player in team['Players']:
                if player['Subject'] == self.uuid:
                    self.agent_name = utils.agent_ids[player['CharacterID']]
        print(presence_data)
        self.client.set_activity(
            state=presence_data['party_state'],
            details="Agent Select" + (f" - {self.mode}" if self.mode else ""),
            start = presence_data['time'] if not presence_data['time'] == False else None,
            large_image=f"agent_{self.agent_name.lower()}",
            large_text=self.agent_name,
            small_image=utils.mode_images[self.mode.lower()],
            party_id=presence_data["partyId"],
            party_size=presence_data['party_size'],
            join=presence_data['join_state']
        )
        
    def mainloop(self,presence_data):
        if self.state == "PREGAME":
            self.pregame_loop(presence_data)





'''
        #agent select
        elif data["sessionLoopState"] == "PREGAME":
            

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