import requests

from ..localization.localization import Localizer

class Loader:

    @staticmethod 
    def fetch(endpoint="/"):
        data = requests.get(f"https://valorant-api.com/v1{endpoint}?language=all")
        return data.json()

    @staticmethod
    def fetch_public_content():
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }
        data = requests.get(f"https://api.henrikdev.xyz/valorant/v1/content",headers=headers) #thanks henrik
        return data.json()

    @staticmethod 
    def load_all_content(client):
        content_data = {
            "agents": [],
            "maps": [],
            "modes": [],   
            "comp_tiers": [],
            "season": {},
            "queue_aliases": { #i'm so sad these have to be hardcoded but oh well :(
                "newmap": "New Map",
                "competitive": "Competitive",
                "unrated": "Unrated",
                "spikerush": "Spike Rush",
                "deathmatch": "Deathmatch",
                "ggteam": "Escalation",
                "onefa": "Replication",
                "custom": "Custom",
                "snowball": "Snowball Fight",
                "": "Custom",
            },
            "team_aliases": {
                "TeamOne": "Defender",
                "TeamTwo": "Attacker",
                "TeamSpectate": "Observer",
                "TeamOneCoaches": "Defender Coach",
                "TeamTwoCoaches": "Attacker Coach",
            },
            "team_image_aliases": {
                "TeamOne": "team_defender",
                "TeamTwo": "team_attacker",
                "Red": "team_defender",
                "Blue": "team_attacker",
            },
            "modes_with_icons": ["ggteam","onefa","snowball","spikerush","unrated","deathmatch"]
        }
        public_content = Loader.fetch_public_content()
        agents = Loader.fetch("/agents")["data"]
        maps = Loader.fetch("/maps")["data"]
        modes = Loader.fetch("/gamemodes")["data"]
        comp_tiers = Loader.fetch("/competitivetiers")["data"][-1]["tiers"]
        

        for season in public_content["acts"]:
            if season["isActive"] and season["type"] == "act":
                content_data["season"] = {
                    "competitive_uuid": season["id"],
                    "season_uuid": season["id"],
                    "display_name": season["name"]
                }

        for agent in agents:
            content_data["agents"].append({
                "uuid": agent["uuid"],
                "display_name": agent["displayName"]["en-US"],
                "display_name_localized": agent["displayName"][Localizer.locale],
                "internal_name": agent["developerName"]
            })

        for game_map in maps:
            content_data["maps"].append({
                "uuid": game_map["uuid"],
                "display_name": game_map["displayName"]["en-US"],
                "display_name_localized": game_map["displayName"][Localizer.locale],
                "path": game_map["mapUrl"],
                "internal_name": game_map["mapUrl"].split("/")[-1]
            })

        for mode in modes:
            content_data["modes"].append({
                "uuid": mode["uuid"],
                "display_name": mode["displayName"]["en-US"],
                "display_name_localized": mode["displayName"][Localizer.locale],
            })

        for tier in comp_tiers:
            content_data["comp_tiers"].append({
                "display_name": tier["tierName"]["en-US"],
                "display_name_localized": tier["tierName"][Localizer.locale],
                "id": tier["tier"],
            })

        return content_data