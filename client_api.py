import re
import aiohttp
import asyncio
import requests
import json
import os

async def auth(username,password):
    session = aiohttp.ClientSession() 
    data = {
        'client_id': 'play-valorant-web-prod',
        'nonce': '1',
        'redirect_uri': 'https://playvalorant.com/opt_in',
        'response_type': 'token id_token',
    }
    await session.post('https://auth.riotgames.com/api/v1/authorization', json=data)

    data = {
        'type': 'auth',
        'username': username,
        'password': password
    }
    async with session.put('https://auth.riotgames.com/api/v1/authorization', json=data) as r:
        data = await r.json()
    #print(data)
    pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
    data = pattern.findall(data['response']['parameters']['uri'])[0]
    access_token = data[0]
    #print('Access Token: ' + access_token)
    id_token = data[1]
    expires_in = data[2]

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    async with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
        data = await r.json()
    entitlements_token = data['entitlements_token']
    #print('Entitlements Token: ' + entitlements_token)

    async with session.post('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
        data = await r.json()
    user_id = data['sub']
    #print('User ID: ' + user_id)
    headers['X-Riot-Entitlements-JWT'] = entitlements_token
    await session.close()
    return user_id, headers

async def get_auth(user, passw): 
    user_id,headers = await auth(user, passw)
    return user_id,headers

def get_glz(endpoint,headers):
    r = requests.get(f'https://glz-na-1.na.a.pvp.net{endpoint}', headers=headers)
    print(r.text)
    data = json.loads(r.text)
    return data

def get_pd(endpoint,headers):
    with requests.get(f'https://pd.na.a.pvp.net{endpoint}', headers=headers) as r:
        data = json.loads(r.text)
    return data

def post_glz(endpoint,headers,data=None):
    r = requests.post(f'https://glz-na-1.na.a.pvp.net{endpoint}', headers=headers, data=data)
    print(r)
    data = json.loads(r.text)
    return data

def post_pd(endpoint,headers,data=None):
    with requests.post(f'https://pd.na.a.pvp.net{endpoint}', headers=headers, data=data) as r:
        data = json.loads(r.text)
>>>>>>> Stashed changes
    return data