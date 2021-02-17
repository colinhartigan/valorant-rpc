import api
import asyncio
import json
import base64
import ssl
import iso8601
import websockets
from pypresence import Presence
import time
import urllib3
urllib3.disable_warnings()

client_id = "811469787657928704"
RPC = Presence(client_id)
RPC.connect()

def parse_time(time):
    split = time.split("-")
    split[0] = split[0].replace(".","-")
    split[1] = split[1].replace(".",":")
    split = "T".join(i for i in split)
    split = iso8601.parse_date(split).timestamp()
    print(split)
    return split

def update_rpc(state):
    data = json.loads(base64.b64decode(state))
    print(data)
    if data["sessionLoopState"] == "MENUS":
        RPC.update(
            state="Not in a Party"+(" (open)" if not data["partyAccessibility"] == "CLOSED" else ""),
            details="In the Menus",
            start=parse_time(data["queueEntryTime"]),
            large_image="game_icon"
        )


lockfile = api.get_lockfile()

while True:
    presence = api.get_presence(lockfile)
    update_rpc(presence)
    time.sleep(3)