import time

from ..menu_presences.away import presence as away
from ...presence_utilities import Utilities
from ....localization.localization import Localizer

class Range_Session:

    def __init__(self,rpc,client,data,match_id,content_data,config):
        self.rpc = rpc
        self.client = client
        self.config = config
        self.content_data = content_data
        self.match_id = match_id  
        self.puuid = self.client.puuid

        data["MapID"] = "/Game/Maps/Poveglia/Range" # hotfix :)
        self.start_time = time.time()
        self.map_name, self.mode_name = Utilities.fetch_map_data(data, content_data)
        self.map_image = "splash_range"
        self.small_image = "mode_unrated"
        self.small_text = None

        if Localizer.get_config_value("presences","modes","range","show_rank_in_range"):
            self.small_image, self.small_text = Utilities.fetch_rank_data(self.client,self.content_data)

    def main_loop(self):
        presence = self.client.fetch_presence()
        while presence is not None and presence["sessionLoopState"] == "INGAME":
            try:
                presence = self.client.fetch_presence()
                is_afk = presence["isIdle"]
                if is_afk:
                    away(self.rpc,self.client,presence,self.content_data,self.config)  
                else:
                    party_state,party_size = Utilities.build_party_state(presence)

                    self.rpc.update(
                        state=party_state,
                        details=self.mode_name,
                        start=self.start_time,
                        large_image=self.map_image,
                        large_text=self.map_name,
                        small_image=self.small_image,
                        small_text=self.small_text,
                        party_size=party_size,
                        party_id=presence["partyId"],
                    )

                time.sleep(Localizer.get_config_value("presence_refresh_interval"))
            except:
                return