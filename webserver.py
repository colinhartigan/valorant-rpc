from flask import Flask 
from flask import request
import json
import threading
import urllib3
urllib3.disable_warnings()
app = Flask(__name__)

@app.route('/')
def success():
    id = request.args.get('code')
    return 'ok'

def start():
    app.run(port=6969)

def run():
    threading.Thread(target=start).start()