<<<<<<< Updated upstream
import requests
import json
from dotenv import load_dotenv
import os
import utils

load_dotenv()

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

client_secret = os.environ.get('CLIENT_SECRET')
api_endpoint = 'https://discord.com/api/v8'

def exchange_code(code):
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:6969',
        'scope': 'rpc'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % api_endpoint, data=data, headers=headers)
    r.raise_for_status()
    with open('config.json','r+') as f:
        data = json.load(f)
        data['rpc-oauth'] = r.json()
        f.seek(0)
        json.dump(data,f,indent=4)
        f.truncate()
        f.close() 
    return r.json()

def refresh_token(refresh_token):
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'redirect_uri': 'http://127.0.0.1:6969',
        'scope': 'rpc'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % api_endpoint, data=data, headers=headers)
    r.raise_for_status()
    with open('config.json','r+') as f:
        data = json.load(f)
        data['rpc-oauth'] = r.json()
        f.seek(0)
        json.dump(data,f,indent=4)
        f.truncate()
        f.close() 
    return r.json()


def authorize(client):
    config = utils.get_config()
    if config['rpc-oauth'] == {}:
        print("authenticating")
        auth = client.authorize(client_id,['rpc'])
        config = utils.get_config()
        code_grant = auth['data']['code']
        result = exchange_code(code_grant)
        client.authenticate(result['access_token'])
    else:
        print("already authenticated!")
        new_token = refresh_token(config['rpc-oauth']['refresh_token'])
=======
import requests
import json
from dotenv import load_dotenv
import os
import utils

load_dotenv()

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

client_secret = os.environ.get('CLIENT_SECRET')
api_endpoint = 'https://discord.com/api/v8'

def exchange_code(code):
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:6969',
        'scope': 'rpc'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % api_endpoint, data=data, headers=headers)
    r.raise_for_status()
    with open('config.json','r+') as f:
        data = json.load(f)
        data['rpc-oauth'] = r.json()
        f.seek(0)
        json.dump(data,f,indent=4)
        f.truncate()
        f.close() 
    return r.json()

def refresh_token(refresh_token):
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'redirect_uri': 'http://127.0.0.1:6969',
        'scope': 'rpc'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % api_endpoint, data=data, headers=headers)
    r.raise_for_status()
    with open('config.json','r+') as f:
        data = json.load(f)
        data['rpc-oauth'] = r.json()
        f.seek(0)
        json.dump(data,f,indent=4)
        f.truncate()
        f.close() 
    return r.json()


def authorize(client):
    config = utils.get_config()
    if config['rpc-oauth'] == {}:
        print("authenticating")
        auth = client.authorize(client_id,['rpc'])
        config = utils.get_config()
        code_grant = auth['data']['code']
        result = exchange_code(code_grant)
        client.authenticate(result['access_token'])
    else:
        print("already authenticated!")
        new_token = refresh_token(config['rpc-oauth']['refresh_token'])
>>>>>>> Stashed changes
        client.authenticate(new_token['access_token'])