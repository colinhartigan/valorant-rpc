
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