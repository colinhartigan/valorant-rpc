

def presence(rpc,client=None,data=None,content_data=None):
    rpc.update(
        state="Loading",
        large_image="game_icon",
        large_text="VALORANT-rpc",
        buttons=[{
            'label':"View on GitHub",
            'url':"https://github.com/colinhartigan/valorant-rpc"
        }]
    )