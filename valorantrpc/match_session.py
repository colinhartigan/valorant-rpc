from . import utils,client_api,riot_api
from .exceptions import AuthError
import os
import asyncio
import time

class Session:
    def __init__(self,client):
        self.loop = asyncio.get_event_loop()
        self.config = utils.get_config()
        self.lockfile = riot_api.get_lockfile()
        self.client = client
        self.uuid = None 
        self.match_id = None
        self.agent_name = ""
        self.map = ""
        self.state = ""
        self.mode = ""
        self.match_start = 0
        self.state_end_time = 0
        self.state_start_time = 0
        self.selected = False
        

    def init_pregame(self,presence_data):
        self.uuid,headers = riot_api.get_auth(self.lockfile)
        pregame_player = client_api.get_glz(f'/pregame/v1/players/{self.uuid}',headers)
        self.match_id = pregame_player['MatchID']
        self.state = "PREGAME"
        self.map = utils.maps[presence_data["matchMap"].split("/")[-1]]
        self.mode = presence_data['queue_id']

    def init_ingame(self,presence_data):
        self.uuid,headers = riot_api.get_auth(self.lockfile)
        coregame_data = client_api.get_glz(f'/core-game/v1/players/{self.uuid}',headers) 
        self.match_id = coregame_data['MatchID']
        match_data = client_api.get_glz(f'/core-game/v1/matches/{self.match_id}',headers)
        self.state = "INGAME"
        self.map = utils.maps[presence_data["matchMap"].split("/")[-1]]
        self.mode = presence_data['queue_id']
        self.state_start_time = presence_data['time'] if presence_data['time'] is not False else time.time()
        for player in match_data['Players']:
            if player['Subject'] == self.uuid:
                self.agent_name = utils.agent_ids[player['CharacterID'].lower()]

        #print(coregame_data)


    def pregame_loop(self,presence_data):
        uuid,headers = riot_api.get_auth(self.lockfile)
        pregame_data = client_api.get_glz(f'/pregame/v1/matches/{self.match_id}',headers)
        if ('PhaseTimeRemainingNS' in pregame_data and pregame_data['PhaseTimeRemainingNS'] == 0) or ('httpStatus' in pregame_data and pregame_data['httpStatus'] == 404):
            self.state = "INGAME"
            self.state_start_time = time.time()
            self.agent_name = "" #just in case the player picks an agent last second and the presence doesnt update before the match loads 
            return

        for team in pregame_data['Teams']:
            for player in team['Players']:
                if player['Subject'] == self.uuid:
                    self.agent_name = utils.agent_ids[player['CharacterID'].lower()]
                    self.selected = True if player['CharacterSelectionState'] == 'locked' else False
        
        if self.uuid in pregame_data['ObserverSubjects']:
            self.agent_name = "Observer"
            
        self.state_end_time = (pregame_data['PhaseTimeRemainingNS'] // 1000000000) + time.time() #why the heck does riot give agent select remaining time in nanoseconds!?!?

        self.client.set_activity(
            state=presence_data['party_state'],
            details="Pregame" + (f" - {self.mode}" if self.mode else ""),
            end=self.state_end_time,
            large_image=f"agent_{self.agent_name.lower()}" if (self.agent_name != "Selecting" and self.agent_name != "Observer") else "game_icon_white",
            large_text=("Selecting - " if not self.selected else "Locked - ") + f"{self.agent_name}" ,
            small_image=utils.mode_images[self.mode.lower()],
            small_text = f"{self.mode}" if self.mode else "",
            party_id=presence_data["partyId"],
            party_size=presence_data['party_size'],
            join=presence_data['join_state']
        )

    def ingame_loop(self,presence_data):
        uuid,headers="",{}
        if presence_data['sessionLoopState'] == 'MENUS':
            self.state = "MENUS"
        try:
            uuid,headers = riot_api.get_auth(self.lockfile)
        except AuthError:
            return
        
        if self.agent_name == "":
            # sometimes it doesn't catch the agent in pregame, so check ingame too
            match_data = client_api.get_glz(f'/core-game/v1/matches/{self.match_id}',headers)
            for player in match_data['Players']:
                if player['Subject'] == self.uuid:
                    self.agent_name = utils.agent_ids[player['CharacterID'].lower()]

        self.map = utils.maps[presence_data["matchMap"].split("/")[-1]]
        score = [presence_data["partyOwnerMatchScoreAllyTeam"],presence_data["partyOwnerMatchScoreEnemyTeam"]]
        self.client.set_activity(
            state=presence_data['party_state'],
            details=f"{self.mode.upper()}: {score[0]} - {score[1]}",
            start=self.state_start_time,
            large_image=f"splash_{self.map.lower()}_square",
            large_text=self.map,
            small_image=f"agent_{self.agent_name.lower()}" if self.agent_name != "Observer" else "game_icon_white",
            small_text = f"{self.agent_name}",
            party_id=presence_data["partyId"],
            party_size=presence_data['party_size'],
            join=presence_data['join_state']
        )

    
    def mainloop(self,presence_data):
        if self.state == "PREGAME":
            self.pregame_loop(presence_data)
        if self.state == "INGAME":
            self.ingame_loop(presence_data)