import requests
import json
from dotenv import load_dotenv
import os
from . import utils
from valorantrpc.exceptions import AuthError

api_endpoint = 'https://discord.com/api/v8'

def exchange_code(code,client_id,client_secret):
    appdata_path = os.path.join(os.getenv('APPDATA'),'valorant-rpc')
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
    with open(os.path.join(appdata_path, 'config.json'), 'r+') as f:
        data = json.load(f)
        data['rpc-oauth'] = r.json()
        f.seek(0)
        json.dump(data,f,indent=4)
        f.truncate()
        f.close() 
    return r.json()

def refresh_token(refresh_token,client_id,client_secret):
    appdata_path = os.path.join(os.getenv('APPDATA'),'valorant-rpc')
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
    with open(os.path.join(appdata_path, 'config.json'), 'r+') as f:
        data = json.load(f)
        data['rpc-oauth'] = r.json()
        f.seek(0)
        json.dump(data,f,indent=4)
        f.truncate()
        f.close() 
    return r.json()


def authorize(client,client_id,client_secret):
    config = utils.get_config()
    if config['rpc-oauth'] == {}:
        try:
            print("[i] authorizing with discord")
            auth = client.authorize(client_id,['rpc'])
            config = utils.get_config()
            code_grant = auth['data']['code']
            result = exchange_code(code_grant,client_id,client_secret)
            client.authenticate(result['access_token'])
        except Exception as e:
            print(e)
            raise AuthError
    else:
        try:
            print("[i] already authorized with discord! refreshing token...")
            new_token = refresh_token(config['rpc-oauth']['refresh_token'],client_id,client_secret)
            client.authenticate(new_token['access_token'])
        except:
            raise AuthError