import time

from ...presence_utilities import Utilities
from ..menu_presences.away import presence as away
from ....localization.localization import Localizer
from valclient.exceptions import PhaseError

class Game_Session:

    def __init__(self,rpc,client,data,match_id,content_data,config):
        self.rpc = rpc
        self.client = client
        self.config = config
        self.content_data = content_data
        self.match_id = match_id 
        self.puuid = self.client.puuid

        self.start_time = time.time()
        self.large_text = ""
        self.large_image = ""
        self.small_text = ""
        self.small_image = ""
        self.mode_name = ""

        self.large_pref = Localizer.get_config_value("presences","modes","all","large_image",0)
        self.small_pref = Localizer.get_config_value("presences","modes","all","small_image",0)

        self.build_static_states()

    def build_static_states(self):
        # generate agent, map etc.
        presence = self.client.fetch_presence()
        try:
            coregame_data = self.client.coregame_fetch_match(self.match_id)
        except PhaseError:
            raise Exception
        coregame_player_data = {}
        for player in coregame_data["Players"]:
            if player["Subject"] == self.puuid:
                coregame_player_data = player

        self.large_image, self.large_text = Utilities.get_content_preferences(self.client,self.large_pref,presence,coregame_player_data,coregame_data,self.content_data)
        self.small_image, self.small_text = Utilities.get_content_preferences(self.client,self.small_pref,presence,coregame_player_data,coregame_data,self.content_data)
        _, self.mode_name = Utilities.fetch_mode_data(presence,self.content_data)

    def main_loop(self):
        presence = self.client.fetch_presence()
        while presence is not None and presence["sessionLoopState"] == "INGAME":
            presence = self.client.fetch_presence()
            is_afk = presence["isIdle"]
            if is_afk:
                away(self.rpc,self.client,presence,self.content_data,self.config)  
            else:
                party_state,party_size = Utilities.build_party_state(presence)
                my_score,other_score = presence["partyOwnerMatchScoreAllyTeam"],presence["partyOwnerMatchScoreEnemyTeam"]

                self.rpc.update(
                    state=party_state,
                    details=f"{self.mode_name} // {my_score} - {other_score}",
                    start=self.start_time,
                    large_image=self.large_image,
                    large_text=self.large_text,
                    small_image=self.small_image,
                    small_text=self.small_text,
                    party_size=party_size,
                    party_id=presence["partyId"],
                    instance=True,
                )

            time.sleep(Localizer.get_config_value("presence_refresh_interval"))