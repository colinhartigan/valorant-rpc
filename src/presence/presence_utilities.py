import iso8601


class Utilities:

    @staticmethod 
    def build_party_state(data):
        party_state = "Solo"       
        if data["partySize"] > 1:
            party_state = "In a Party"
        elif data["partyAccessibility"] == "OPEN":
            party_state = "Open Party"

        party_size = [data["partySize"],data["maxPartySize"]] if data["partySize"] > 1 or data["partyAccessibility"] == "OPEN" else None
        return party_state, party_size 

    @staticmethod 
    def iso8601_to_epoch(time):
        if time == "0001.01.01-00.00.00":
            return None
        split = time.split("-")
        split[0] = split[0].replace(".","-")
        split[1] = split[1].replace(".",":")
        split = "T".join(i for i in split)
        split = iso8601.parse_date(split).timestamp() #converts iso8601 to epoch
        return split

    @staticmethod 
    def fetch_rank_data(client,content_data):
        mmr = client.fetch_mmr()["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][content_data["season"]["season_uuid"]]
        rank_data = {}
        for tier in content_data["comp_tiers"]:
            if tier["id"] == mmr["CompetitiveTier"]:
                rank_data = tier
        rank_image = f"rank_{rank_data['id']}"
        rank_text = f"{rank_data['display_name']} - {mmr['RankedRating']}RR"

        return rank_image, rank_text
        
    @staticmethod 
    def fetch_map_data(data,content_data):
        for gmap in content_data["maps"]:
            if gmap["path"] == data["matchMap"]:
                return gmap["display_name"]
        return ""
 
    @staticmethod 
    def fetch_agent_data(uuid,content_data):
        for agent in content_data["agents"]:
            if agent["uuid"] == uuid:
                agent_image = f"agent_{agent['display_name'].lower().replace('/','')}"
                agent_name = agent['display_name']
                return agent_image, agent_name
        return "rank_0","A Secret Agent"

    @staticmethod
    def fetch_mode_data(data, content_data):
        image = f"mode_{data['queueId'] if data['queueId'] in content_data['modes_with_icons'] else 'discovery'}"
        mode_name = content_data['queue_aliases'][data['queueId']] if data["queueId"] in content_data["queue_aliases"].keys() else "Custom"
        return image,mode_name

    @staticmethod 
    def get_content_preferences(client,pref,presence,player_data,content_data):
        if pref == "rank":
            return Utilities.fetch_rank_data(client,content_data)
        if pref == "map": 
            gmap = Utilities.fetch_map_data(presence,content_data)
            return f"splash_{gmap.lower()}",gmap
        if pref == "agent": 
            return Utilities.fetch_agent_data(player_data["CharacterID"],content_data)

    @staticmethod 
    def get_join_state(client,config,presence=None):
        if presence is None:
            presence = client.fetch_presence()
        base_api_url = "https://colinhartigan.github.io/valorant-rpc?redir={redirect}&type={type}"
        base_api_url = f"{base_api_url}&region={client.region}&playername={client.player_name}&playertag={client.player_tag}" # add on static values (region/playername)
        if int(presence["partySize"]) < int(presence["maxPartySize"]):
            if presence["partyAccessibility"] == "OPEN" and config["presences"]["menu"]["show_join_button_with_open_party"]:
                return [{"label":"Join","url":base_api_url.format(redirect=f"/valorant/join/{presence['partyId']}",type="join")}]
            
            if presence["partyAccessibility"] == "CLOSED" and config["presences"]["menu"]["allow_join_requests"]:
                return [{"label":"Request to Join","url":base_api_url.format(redirect=f"/valorant/request/{presence['partyId']}/{client.puuid}",type="request")}]

        return None