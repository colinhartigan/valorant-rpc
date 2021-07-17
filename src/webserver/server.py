from flask import Flask, request, cli, jsonify, Response
from flask_cors import CORS
import urllib3, logging

urllib3.disable_warnings()
app = Flask(__name__)
CORS(app)
cli.show_server_banner = lambda *_: None
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# a not-so-rich discord invite system

client = None 
config = None

@app.route('/')
def home():
    return 'ok'


@app.route('/valorant/request/<party_id>/<friend_id>')
def request_party(party_id,friend_id):
    region = request.args.get('region')
    if region == client.region:
        data = client.party_request_to_join(party_id,friend_id)
        for player in data["Requests"]:
            if client.puuid == player["RequestedBySubject"]:
                return "<script>window.onload = window.close();</script>"
        return data
    else:
        return f"you're not in the right region! (their region: {region}, your region: {client.region})"

@app.route('/valorant/join/<party_id>')
def join_party(party_id):
    region = request.args.get('region')
    if region == client.region:
        data = client.party_join(party_id)
        if "CurrentPartyID" in data.keys():
            return "<script>window.onload = window.close();</script>"
        return data

    return f"you're not in the right region! (their region: {region}, your region: {client.region})"


def start():
    app.run(port=4100)
