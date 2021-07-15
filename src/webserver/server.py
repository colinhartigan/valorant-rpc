from flask import Flask, request, cli
import threading, urllib3

urllib3.disable_warnings()
app = Flask(__name__)
cli.show_server_banner = lambda *_: None


@app.route('/')
def success():
    return 'nothin here'

@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'server shutting down...'

@app.route('/request/<party_id>')
def request_party(party_id):
    pass

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()  

def start():
    app.run(port=6969)

def run():
    threading.Thread(target=start).start()