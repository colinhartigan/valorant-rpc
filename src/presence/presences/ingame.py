from ..presence_utilities import Utilities
import time

from .menu_presences.away import presence as away

def presence(rpc,client=None,data=None,content_data=None,config=None):
    coregame = client.coregame_fetch_player()

    if coregame is not None:
        match_id = coregame["MatchID"]
        session = Game_Session(rpc,client,match_id,content_data,config)
        session.main_loop()


class Game_Session:

    def __init__(self,rpc,client,match_id,content_data,config):
        self.rpc = rpc
        self.client = client
        self.config = config
        self.content_data = content_data
        self.match_id = match_id 
        self.puuid = self.client.puuid

        self.agent_name = ""
        self.agent_image = ""
        self.map_name = ""
        self.map_image = ""
        self.mode_name = ""

        self.build_static_states()

    def build_static_states(self):
        # generate agent, map etc.
        presence = self.client.fetch_presence()
        coregame_data = self.client.coregame_fetch_match(self.match_id)
        coregame_player_data = {}
        for player in coregame_data["Players"]:
            if player["Subject"] == self.puuid:
                coregame_player_data = player

        self.map_name = Utilities.fetch_map_data(presence,self.content_data)
        self.map_image = f"splash_{self.map_name.lower()}"
        _, self.mode_name = Utilities.fetch_mode_data(presence,self.content_data)
        self.agent_image, self.agent_name = Utilities.fetch_agent_data(coregame_player_data["CharacterID"],self.content_data)



    def main_loop(self):
        while self.client.fetch_presence()["sessionLoopState"] == "INGAME":
            presence = self.client.fetch_presence()
            is_afk = presence["isIdle"]
            if is_afk:
                away(self.rpc,self.client,presence,self.content_data,self.config)  

            party_state,party_size = Utilities.build_party_state(presence)
            my_score,other_score = presence["partyOwnerMatchScoreAllyTeam"],presence["partyOwnerMatchScoreEnemyTeam"]
            start_time = Utilities.iso8601_to_epoch(presence['queueEntryTime'])

            self.rpc.update(
                state=party_state,
                details=f"{self.mode_name} // {my_score} - {other_score}",
                start=start_time,
                large_image=self.map_image,
                large_text=self.map_name,
                small_image=self.agent_image,
                small_text=self.agent_name,
                party_size=party_size,
                party_id=presence["partyId"],
            )

            time.sleep(self.config["presence_refresh_interval"])
        