import re
import aiohttp
import asyncio
import requests
import json
import os
from .exceptions import AuthError

def get_glz(endpoint,headers):
    r = requests.get(f'https://glz-na-1.na.a.pvp.net{endpoint}', headers=headers)
    data = json.loads(r.text)
    return data

def get_pd(endpoint,headers):
    r = requests.get(f'https://pd.na.a.pvp.net{endpoint}', headers=headers)
    data = json.loads(r.text)
    return data

def post_glz(endpoint,headers,data=None):
    r = requests.post(f'https://glz-na-1.na.a.pvp.net{endpoint}', headers=headers, data=data)
    data = json.loads(r.text)
    return data

def post_pd(endpoint,headers,data=None):
    r = requests.post(f'https://pd.na.a.pvp.net{endpoint}', headers=headers, data=data)
    data = json.loads(r.text)
    return data