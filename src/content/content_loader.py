import requests

class Loader:

    @staticmethod 
    def fetch(endpoint="/"):
        data = requests.get(f"https://valorant-api.com/v1{endpoint}")
        return data.json()

    @staticmethod 
    def load_all_content(client):
        content_data = {
            "agents": [],
            "maps": [],
            "modes": [],   
            "comp_tiers": [],
            "queue_aliases": { #i'm so sad these have to be hardcoded but oh well :(
                "newmap": "New Map",
                "competitive": "Competitive",
                "unrated": "Unrated",
                "spikerush": "Spike Rush",
                "deathmatch": "Deathmatch",
                "ggteam": "Escalation",
                "onefa": "Replication",
                "custom": "Custom",
                "snowball": "Snowball Fight"
            },
            "modes_with_icons": ["deathmatch","ggteam","onefa","snowball","spikerush","unrated"]
        }
        agents = Loader.fetch("/agents")["data"]
        maps = Loader.fetch("/maps")["data"]
        modes = Loader.fetch("/gamemodes")["data"]
        comp_tiers = Loader.fetch("/competitivetiers")["data"][-1]["tiers"]
        
        for agent in agents:
            content_data["agents"].append({
                "uuid": agent["uuid"],
                "display_name": agent["displayName"],
                "internal_name": agent["developerName"]
            })

        for game_map in maps:
            content_data["maps"].append({
                "uuid": game_map["uuid"],
                "display_name": game_map["displayName"],
                "path": game_map["mapUrl"],
                "internal_name": game_map["mapUrl"].split("/")[-1]
            })

        for mode in modes:
            content_data["modes"].append({
                "uuid": mode["uuid"],
                "display_name": mode["displayName"],
            })

        for tier in comp_tiers:
            content_data["comp_tiers"].append({
                "display_name": tier["tierName"],
                "id": tier["tier"],
            })

        return content_data