import iso8601

maps = {
    "Port":"Icebox",
    "Duality":"Bind",
    "Bonsai":"Split",
    "Ascent":"Ascent",
    "Triad":"Haven",
    "Range":"Range"
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
    "spikerush":"mode_spike_rush",
    "deathmatch":"mode_deathmatch",
    "ggteam":"mode_escalation",
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


validate_party_size = lambda data : data["isPartyOwner"] == True and data["partySize"] > 1