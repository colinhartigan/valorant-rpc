import iso8601
import json
import ctypes
import psutil
from psutil import AccessDenied
import sys
import os
from datetime import datetime
import requests

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()

maps = {
    "Port":"Icebox",
    "Duality":"Bind",
    "Bonsai":"Split",
    "Ascent":"Ascent",
    "Triad":"Haven",
    "Foxtrot":"Breeze",
    "Range":"Range",
    "":"game_icon"
}
queue_ids = {
    "unrated":"Unrated",
    "competitive":"Competitive",
    "spikerush":"Spike Rush",
    "deathmatch":"Deathmatch",
    "ggteam":"Escalation",
    "newmap":"Breeze",
    "":""
}
mode_images = {
    "unrated":"mode_standard",
    "competitive":"mode_standard",
    "spike rush":"mode_spike_rush",
    "deathmatch":"mode_deathmatch",
    "escalation":"mode_escalation",
    "newmap":"mode_standard",
    "custom":"mode_standard",
}
agent_ids = {
    "5f8d3a7f-467b-97f3-062c-13acf203c006":"Breach",
    "f94c3b30-42be-e959-889c-5aa313dba261":"Raze",
    "6f2a04ca-43e0-be17-7f36-b3908627744d":"Skye",
    "117ed9e3-49f3-6512-3ccf-0cada7e3823b":"Cypher",
    "320b2a48-4d9b-a075-30f1-1f93a9b638fa":"Sova",
    "1e58de9c-4950-5125-93e9-a0aee9f98746":"Killjoy",
    "707eab51-4836-f488-046a-cda6bf494859":"Viper",
    "eb93336a-449b-9c1b-0a54-a891f7921d69":"Phoenix",
    "41fb69c1-4189-7b37-f117-bcaf1e96f1bf":"Astra",
    "9f0d8ba9-4140-b941-57d3-a7ad57c6b417":"Brimstone",
    "7f94d92c-4234-0a36-9646-3a87eb8b5c89":"Yoru",
    "569fdd95-4d10-43ab-ca70-79becc718b46":"Sage",
    "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc":"Reyna",
    "8e253930-4c05-31dd-1b6c-968525494517":"Omen",
    "add6443a-41bd-e414-f6ad-e58d267f4e95":"Jett",
    "":"?"
}


#weird workaround for getting image w/ relative path to work with pyinstaller
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'): 
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_latest_github_release_tag():
    data = requests.get("https://api.github.com/repos/colinhartigan/valorant-rpc/releases/latest")
    latest = data.json()["tag_name"]
    return latest


#------------------------------------------------------------------------------------------------
# config stuff
def get_config():
    appdata_path = os.path.join(os.getenv('APPDATA'),'valorant-rpc')
    if not os.path.exists(appdata_path):
        os.makedirs(appdata_path)
    try:
        with open(get_resource_path(os.path.join(appdata_path, 'config.json'))) as f:     
            data = json.loads(f.read())
            return data
    except FileNotFoundError as e:
        print(f'[!] config.json not found! generating a new one @ {appdata_path}...')
        #generate a config in appdata

        with open(get_resource_path(os.path.join(appdata_path, 'config.json')), 'w') as f:
            payload = get_blank_config()
            json.dump(payload,f,indent=4)

        return get_config()


def create_new_config():
    appdata_path = os.path.join(os.getenv('APPDATA'),'valorant-rpc')
    old_config = get_config()

    # rename old config, replace old config if there was already one
    if os.path.exists(get_resource_path(os.path.join(appdata_path, 'old_config.json'))):
        os.remove(get_resource_path(os.path.join(appdata_path, 'old_config.json')))

    os.rename(get_resource_path(os.path.join(appdata_path, 'config.json')),get_resource_path(os.path.join(appdata_path, 'old_config.json')))

    print(f'[i] creating new config @ {appdata_path}; make sure you update your settings')
    # create new config
    with open(get_resource_path(os.path.join(appdata_path, 'config.json')), 'w') as f:
        payload = get_blank_config()
        json.dump(payload,f,indent=4)

    return get_config()


def get_blank_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(get_resource_path(os.path.join(dir_path, '../data/blank_config.json'))) as f:
        return json.loads(f.read())
#------------------------------------------------------------------------------------------------


def sanitize_presence(original):
    try:
        data = original
        data["party_state"] = "Solo" 
        if data["partySize"] > 1:
            data["party_state"] = "In a Party"
        data["party_state"] = "Open Party" if not data["partyAccessibility"] == "CLOSED" else data["party_state"]

        data["queue_id"] = queue_ids[data["queueId"]]
        if data["partyState"] == "CUSTOM_GAME_SETUP":
            data["queue_id"] = "Custom"

        data["party_size"] = [data["partySize"],data["maxPartySize"]] if data["partySize"] > 1 or data["partyAccessibility"] == "OPEN" else None

        #queue timing stuff
        data["time"] = iso8601_to_epoch(data["queueEntryTime"])
        if not data["partyState"] == "MATCHMAKING" and not data["sessionLoopState"] == "INGAME" and not data["partyState"] == "MATCHMADE_GAME_STARTING" and not data["sessionLoopState"] == "PREGAME":
            data["time"] = False
        if data["partyState"] == "CUSTOM_GAME_SETUP":
            data["time"] = False

        data["join_state"] = f"partyId/{data['partyId']}" if data["partyAccessibility"] == "OPEN" else None

        data["map_name"] = maps[data["matchMap"].split("/")[-1]]
        return data
    except:
        return original


def get_current_version():
    data = requests.get('https://valorant-api.com/v1/version')
    data = data.json()['data']
    version = f"{data['branch']}-shipping-{data['buildVersion']}-{data['version'].split('.')[3]}"
    return version


def iso8601_to_epoch(time):
    if time == "0001.01.01-00.00.00":
        return False
    split = time.split("-")
    split[0] = split[0].replace(".","-")
    split[1] = split[1].replace(".",":")
    split = "T".join(i for i in split)
    split = iso8601.parse_date(split).timestamp() #converts iso8601 to epoch
    return split

def seconds_to_iso8601(seconds):
    dt = datetime.fromtimestamp(seconds)
    print(dt.isoformat())


def is_process_running(required_processes=["VALORANT-Win64-Shipping.exe", "RiotClientServices.exe"]):
    processes = []
    running_count = 0
    for proc in psutil.process_iter():
        try:
            processes.append(proc.name())
        except (PermissionError, AccessDenied):
            pass 
    for process in required_processes:
        if process in processes:
            running_count += 1
    if running_count == len(required_processes):
        return True
    else:
        return False

def get_rcs_path():
    # thanks github/afwolfe :)
    '''
    Attempts to use the RiotClientInstalls.json file to detect the location of RiotClientServices.
    Returns the absolute path if found or None if not.
    '''
    RIOT_CLIENT_INSTALLS_PATH = os.path.expandvars("%PROGRAMDATA%\\Riot Games\\RiotClientInstalls.json")
    try:
        with open(RIOT_CLIENT_INSTALLS_PATH, "r") as file:
            client_installs = json.load(file)
            rcs_path = os.path.abspath(client_installs["rc_default"])
            if not os.access(rcs_path, os.X_OK):
                return None
            return rcs_path
    except FileNotFoundError:
        return None


validate_party_size = lambda data : data["isPartyOwner"] == True and data["partySize"] > 1