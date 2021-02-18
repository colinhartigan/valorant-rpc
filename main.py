import api,utils
import asyncio
import json
import base64
import ssl
import websockets
from pypresence import Presence
import time
import urllib3
urllib3.disable_warnings()

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

client_id = "811469787657928704"
RPC = Presence(client_id)
RPC.connect()

last_state = ""
last_queue_time = ""
stop_time = True

def update_rpc(state):
    data = json.loads(base64.b64decode(state))
    print(data)

    #party state
    party_state = "Solo" 
    if data["partySize"] > 1:
        party_state = "In a Party"
    party_state = party_state+(" (open)" if not data["partyAccessibility"] == "CLOSED" else "")

    queue_id = utils.queue_ids[data["queueId"]]
    if data["partyState"] == "CUSTOM_GAME_SETUP":
        queue_id = "Custom"

    party_size = [data["partySize"],data["maxPartySize"]] if not data["partySize"] == 1 else None


    #queue timing stuff
    time = utils.parse_time(data["queueEntryTime"])
    if not data["partyState"] == "MATCHMAKING" and not data["sessionLoopState"] == "INGAME" and not data["partyState"] == "MATCHMADE_GAME_STARTING" and not data["sessionLoopState"] == "PREGAME":
        time = False
    if data["partyState"] == "CUSTOM_GAME_SETUP":
        time = False

 
    if not data["isIdle"]:
        #menu
        if data["sessionLoopState"] == "MENUS" and data["partyState"] != "CUSTOM_GAME_SETUP":
            RPC.update(
                state=party_state,
                details=("In Queue" if data["partyState"] == "MATCHMAKING" else "Lobby") + (f" - {queue_id}" if queue_id else ""),
                start=time if not time == False else None,
                large_image="game_icon",
                large_text="VALORANT",
                small_image="crown_icon" if utils.validate_party_size(data) else None,
                small_text="Party Leader" if utils.validate_party_size(data) else None,
                party_id=data["partyId"],
                party_size=party_size,
            )

        #custom setup
        elif data["sessionLoopState"] == "MENUS" and data["partyState"] == "CUSTOM_GAME_SETUP":
            game_map = utils.maps[data["matchMap"].split("/")[-1]]
            RPC.update(
                state=party_state,
                details="Lobby" + (f" - {queue_id}" if queue_id else ""),
                start=time if not time == False else None,
                large_image=f"splash_{game_map.lower()}",
                large_text=game_map,
                small_image="crown_icon" if utils.validate_party_size(data) else None,
                small_text="Party Leader" if utils.validate_party_size(data) else None,
                party_id=data["partyId"],
                party_size=party_size,
            )

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
                start = time if not time == False else None,
                large_image=f"splash_{game_map.lower()}",
                large_text=game_map,
                small_image=utils.mode_images[queue_id.lower()],
                party_id=data["partyId"],
                party_size=party_size,
            )


    elif data["isIdle"]:
        RPC.update(
            state="Away",
            details="Lobby" + (f" - {queue_id}" if queue_id else ""),
            large_image="game_icon",
            large_text="VALORANT",
        )

    



async def listen():
    async with websockets.connect(f'wss://riot:{lockfile["password"]}@localhost:{lockfile["port"]}', ssl=ssl_context) as websocket:
        await websocket.send('[5, "OnJsonApiEvent_chat_v4_presences"]')   
        while True:
            try:
                response = json.loads(await websocket.recv())
                if response[2]['data']['presences'][0]['puuid'] == api.get_puuid(api.get_lockfile()):
                        update_rpc(response[2]['data']['presences'][0]['private'])
            except:
                pass


if __name__=="__main__":
    
    lockfile = api.get_lockfile()
    presence = api.get_presence(lockfile)
    update_rpc(presence)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(listen())
