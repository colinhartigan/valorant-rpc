from . import utils

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
        self,mode = presence_data['queue_id']

    def pregame_loop(self,presence_data):
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
        self.map = utils.maps[presence_data["matchMap"].split("/")[-1]]
        score = [presence_data["partyOwnerMatchScoreAllyTeam"],presence_data["partyOwnerMatchScoreEnemyTeam"]]
        self.client.set_activity(
            state=presence_data['party_state'],
            details=f"{self.mode.upper()}: {score[0]} - {score[1]}",
            start=presence_data['time'] if not presence_data['time'] == False else None,
            large_image=f"splash_{self.map.lower()}",
            large_text=self.map,
            small_image=utils.mode_images[self.mode.lower()],
            party_id=presence_data["partyId"],
            party_size=presence_data['party_size'],
        )

'''
    #agent select
        elif data["sessionLoopState"] == "PREGAME":
            game_map = utils.maps[data["matchMap"].split("/")[-1]]
            RPC.update(
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
            RPC.update(
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
            RPC.update(
                state=party_state,
                details="THE RANGE",
                large_image=f"splash_{game_map.lower()}",
                large_text=game_map,
                small_image=utils.mode_images[queue_id.lower()],
                party_id=data["partyId"],
                party_size=party_size,
            )
'''
