from ...localization.localization import Localizer

def presence(rpc,client=None,data=None,content_data=None,config=None):
    rpc.update(
        state=Localizer.get_localized_text("presences","startup","loading"),
        large_image="game_icon",
        large_text="VALORANT-rpc",
        buttons=[{
            'label':Localizer.get_localized_text("presences","startup","view_github"),
            'url':"https://github.com/colinhartigan/valorant-rpc"
        }] if Localizer.get_config_value("startup","show_github_link") else None
    )