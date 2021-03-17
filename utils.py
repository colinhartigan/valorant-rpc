import iso8601
import os
import json

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

def parse_time(time):
    if time == "0001.01.01-00.00.00":
        return False
    split = time.split("-")
    split[0] = split[0].replace(".","-")
    split[1] = split[1].replace(".",":")
    split = "T".join(i for i in split)
    split = iso8601.parse_date(split).timestamp()
    return split

def get_rcs_path():
    """Attempts to use the RiotClientInstalls.json file to detect the location of RiotClientServices.
    Returns the absolute path if found or None if not."""
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