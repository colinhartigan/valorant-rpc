import re
import aiohttp
import asyncio
import requests
import json
import os
from .exceptions import AuthError
from valorantrpc import utils

def get_glz(endpoint,headers):
    config = utils.get_config()
    client_region = config["region"]
    r = requests.get(f'https://glz-{client_region}-1.{client_region}.a.pvp.net{endpoint}', headers=headers)
    data = json.loads(r.text)
    return data

def get_pd(endpoint,headers):
    config = utils.get_config()
    client_region = config["region"]
    r = requests.get(f'https://pd.{client_region}.a.pvp.net{endpoint}', headers=headers)
    data = json.loads(r.text)
    return data

def post_glz(endpoint,headers,data=None):
    config = utils.get_config()
    client_region = config["region"]
    r = requests.post(f'https://glz-{client_region}-1.{client_region}.a.pvp.net{endpoint}', headers=headers, data=data)
    data = json.loads(r.text)
    return data

def post_pd(endpoint,headers,data=None):
    config = utils.get_config()
    client_region = config["region"]
    r = requests.post(f'https://pd.{client_region}.a.pvp.net{endpoint}', headers=headers, data=data)
    data = json.loads(r.text)
    return data