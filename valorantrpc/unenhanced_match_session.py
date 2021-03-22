from . import utils
import time

class Session:
    def __init__(self,client):
        self.client = client
        self.map = ""
        self.state = ""
        self.mode = ""

    def init_pregame(self,presence_data):
        self.state = "PREGAME"
        self.mode = presence_data['queue_id']

    def init_ingame(self,presence_data):
        self.state = "INGAME"
        self.mode = presence_data['queue_id']

    def pregame_loop(self,presence_data):
        if presence_data['sessionLoopState'] == "MENUS":
            self.state = "MENUS"
        if presence_data['sessionLoopState'] == "INGAME":
            self.state = "INGAME"
        self.map = utils.maps[presence_data["matchMap"].split("/")[-1]]
        self.client.set_activity(
            state=presence_data['party_state'],
            details="Pregame" + (f" - {self.mode}" if self.mode else ""),
            start=presence_data['time'] if not presence_data['time'] == False else None,
            large_image=f"splash_{self.map.lower()}",
            large_text=self.map,
            small_image=utils.mode_images[self.mode.lower()],
            small_text = f"{self.mode}" if self.mode else "",
            party_id=presence_data["partyId"],
            party_size=presence_data['party_size'],
        )

    def ingame_loop(self,presence_data):
        if presence_data['sessionLoopState'] == "MENUS":
            self.state = "MENUS"
        self.map = utils.maps[presence_data["matchMap"].split("/")[-1]]
        score = [presence_data["partyOwnerMatchScoreAllyTeam"],presence_data["partyOwnerMatchScoreEnemyTeam"]]
        self.client.set_activity(
            state=presence_data['party_state'],
            details=f"{self.mode.upper()}: {score[0]} - {score[1]}",
            start=presence_data['time'] if presence_data['time'] is not False else time.time(),
            large_image=f"splash_{self.map.lower()}",
            large_text=self.map,
            small_image=utils.mode_images[self.mode.lower()],
            party_id=presence_data["partyId"],
            party_size=presence_data['party_size'],
        )

    def mainloop(self,presence_data):
        if self.state == "PREGAME":
            self.pregame_loop(presence_data)
        elif self.state == "INGAME":
            self.ingame_loop(presence_data)
