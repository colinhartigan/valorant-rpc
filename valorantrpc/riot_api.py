import os
import requests
import json
import base64
from valorantrpc.exceptions import AuthError
from valorantrpc import utils

lockfilePath = os.path.join(os.getenv('LOCALAPPDATA'), R'Riot Games\Riot Client\Config\lockfile')

def get_lockfile():
    try:
        with open(lockfilePath) as lockfile:
            data = lockfile.read().split(':')
            keys = ['name', 'PID', 'port', 'password', 'protocol']
            return dict(zip(keys, data))
    except:
        return None

def get_puuid(lockfile):
    try:
        headers = {}
        headers['Authorization'] = 'Basic ' + base64.b64encode(('riot:' + lockfile['password']).encode()).decode()
        response = requests.get("https://127.0.0.1:{port}/chat/v1/session".format(port=lockfile['port']), headers=headers, verify=False)

        return response.json()['puuid']
    except:
        return None
 
def get_presence(lockfile):
    try:
        headers = {}
        headers['Authorization'] = 'Basic ' + base64.b64encode(('riot:' + lockfile['password']).encode()).decode()

        response = requests.get("https://127.0.0.1:{port}/chat/v4/presences".format(port=lockfile['port']), headers=headers, verify=False)
        presences = response.json()

        for presence in presences['presences']:
            if presence['puuid'] == get_puuid(lockfile):
                payload = utils.sanitize_presence(json.loads(base64.b64decode(presence['private'])))
                return payload
    except:
        return None

def get_auth(lockfile):
    try:
        headers = {}
        headers['Authorization'] = 'Basic ' + base64.b64encode(('riot:' + lockfile['password']).encode()).decode()

        response = requests.get("https://127.0.0.1:{port}/entitlements/v1/token".format(port=lockfile['port']), headers=headers, verify=False)
        entitlements = response.json()
        payload = {
            'Authorization': f"Bearer {entitlements['accessToken']}",
            'X-Riot-Entitlements-JWT': entitlements['token'],
            'X-Riot-ClientPlatform': "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
            'X-Riot-ClientVersion': utils.get_current_version()
        }
        return entitlements['subject'],payload
    except:
        raise AuthError