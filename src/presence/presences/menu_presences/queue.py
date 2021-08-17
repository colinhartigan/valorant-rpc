from ...presence_utilities import Utilities
from ....localization.localization import Localizer

def presence(rpc,client=None,data=None,content_data=None,config=None):
    
    party_state,party_size = Utilities.build_party_state(data)
    start_time = Utilities.iso8601_to_epoch(data['queueEntryTime'])

    rpc.update(
        state=party_state,
        details=f"{Localizer.get_localized_text('presences','client_states','queue')} - {content_data['queue_aliases'][data['queueId']]}",
        start=start_time,
        large_image="game_icon_white",
        large_text=f"Level {data['accountLevel']}",
        small_image=f"mode_{data['queueId'] if data['queueId'] in content_data['modes_with_icons'] else 'unrated'}",
        party_size=party_size,
        party_id=data["partyId"],
    )