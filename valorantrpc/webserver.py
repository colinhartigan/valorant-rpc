from flask import Flask 
from flask import request
import json
import threading
import urllib3
import os,sys
urllib3.disable_warnings()
app = Flask(__name__)
from flask import cli
import requests
cli.show_server_banner = lambda *_: None

@app.route('/')
def success():
    id = request.args.get('code')
    return 'ok'

@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'server shutting down...'

def start():
    app.run(port=6969)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()  

def run():
    threading.Thread(target=start).start()

