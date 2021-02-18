import os
import requests
import base64

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
                return presence['private']
    except:
        return None