def presence(rpc,client=None,data=None,content_data=None,config=None):
    rpc.update(
        state="Away",
        details=f"Menu - {content_data['queue_aliases'][data['queueId']] if data['queueId'] != '' else 'Custom Setup'}",
        large_image="game_icon_yellow",
        large_text="VALORANT",
    )