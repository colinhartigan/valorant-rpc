from flask import Flask, request, cli
import urllib3, logging

urllib3.disable_warnings()
app = Flask(__name__)
cli.show_server_banner = lambda *_: None
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

client = None 
config = None

@app.route('/')
def home():
    return 'nothin to see here'

@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'server shutting down...'

@app.route('/valorant/request/<party_id>/<friend_id>')
def request_party(party_id,friend_id):
    data = client.party_request_to_join(party_id,friend_id)
    for player in data["Requests"]:
        if client.puuid == player["RequestedBySubject"]:
            return 'ok'
    return data

@app.route('/valorant/join/<party_id>')
def join_party(party_id):
    data = client.party_join(party_id)
    if "CurrentPartyID" in data.keys():
        return "<script>window.onload = window.close();</script>"
    return data

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()  

def start():
    app.run(port=6969)
