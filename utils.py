import iso8601
import json
import ctypes
import psutil
from psutil import AccessDenied
import sys

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()

maps = {
    "Port":"Icebox",
    "Duality":"Bind",
    "Bonsai":"Split",
    "Ascent":"Ascent",
    "Triad":"Haven",
    "Range":"Range",
    "":"game_icon"
}
queue_ids = {
    "unrated":"Unrated",
    "competitive":"Competitive",
    "spikerush":"Spike Rush",
    "deathmatch":"Deathmatch",
    "ggteam":"Escalation",
    "":""
}
mode_images = {
    "unrated":"mode_standard",
    "competitive":"mode_standard",
    "spike rush":"mode_spike_rush",
    "deathmatch":"mode_deathmatch",
    "escalation":"mode_escalation",
    "custom":"mode_standard",
}

def get_config():
    try:
        with open('config.json') as f:
            return json.loads(f.read())
    except FileNotFoundError as e:
        with open('config.json','w') as f:
            payload = {
                "rpc-oauth": {},
                "riot-account": {
                    "username": "",
                    "password": ""
                }
            }
            json.dump(payload,f,indent=4)
            return get_config()

def parse_time(time):
    if time == "0001.01.01-00.00.00":
        return False
    split = time.split("-")
    split[0] = split[0].replace(".","-")
    split[1] = split[1].replace(".",":")
    split = "T".join(i for i in split)
    split = iso8601.parse_date(split).timestamp()
    return split

def is_process_running(required_processes=["VALORANT-Win64-Shipping.exe", "RiotClientServices.exe"]):
    processes = []
    for proc in psutil.process_iter():
        try:
            processes.append(proc.name())
        except (PermissionError, AccessDenied):
            pass 
    for process in required_processes:
        if process in processes:
            return True
    return False


validate_party_size = lambda data : data["isPartyOwner"] == True and data["partySize"] > 1