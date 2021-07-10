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