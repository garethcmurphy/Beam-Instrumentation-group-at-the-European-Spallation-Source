#!/usr/bin/env python3
import requests
import json
base_url = "https://scicatapi.esss.dk/api/v3/"
login_url = base_url + "Users/login"

filename = "config.json"
if filename:
    with open(filename, 'r') as f:
        config = json.load(f)

r = requests.post(login_url, data=config)

access_token = r.json()
print (access_token["id"])
pid = "20.500.12269%2FBRIGHTNESS%2FBeamInstrumentation0001"

dataset_url = base_url + "Datasets/"+pid+"?access_token="+access_token["id"]
d=requests.get(dataset_url )
print (d.json())
