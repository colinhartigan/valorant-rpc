from ..presence_utilities import Utilities
import time

def presence(rpc,client=None,data=None,content_data=None,config=None):
    party_state,party_size = Utilities.build_party_state(data)
    
    pregame = client.fetch_pregame_from_puuid()
    if pregame is not None:
        match_id = pregame["MatchID"]
        pregame_data = client.fetch_pregame_from_matchid(match_id)
        puuid = client.puuid

        pregame_player_data = {}
        for player in pregame_data["AllyTeam"]["Players"]:
            if player["Subject"] == puuid:
                pregame_player_data = player

        pregame_end_time = (pregame_data['PhaseTimeRemainingNS'] // 1000000000) + time.time()

        agent_image, agent_name = Utilities.fetch_agent_data(pregame_player_data["CharacterID"],content_data)
        select_state = "Locked" if pregame_player_data["CharacterSelectionState"] == "locked" else "Selecting"

        rpc.update(
            state=party_state,
            details=f"Pregame - {content_data['queue_aliases'][data['queueId']] if data['queueId'] != '' else 'Custom'}",
            end=pregame_end_time,
            large_image=agent_image,
            large_text=f"{select_state} - {agent_name}",
            small_image=f"mode_{data['queueId'] if data['queueId'] in content_data['modes_with_icons'] else 'unrated'}",
            small_text=content_data['queue_aliases'][data['queueId']],
            party_size=party_size,
            party_id=data["partyId"],
        )