#!/usr/bin/env python3
import requests
import json
base_url = "https://scicatapi.esss.dk/"
user_url = base_url + "auth/msad"
api_url = base_url  + "api/v3/"
ingestor_url = api_url+"Users/login"
login_url = user_url

filename = "config.json"
if filename:
    try:
        with open(filename, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Please make a config.json as in config.sample.json")
        print("Exiting")
        exit()

r = requests.post(login_url, data=config)

login_response = r.json()
print (login_response)
token=(login_response["access_token"])
pid = "20.500.12269%2FBRIGHTNESS%2FBeamInstrumentation0001"

dataset_url = api_url + "Datasets/"+pid+"?access_token="+token
d=requests.get(dataset_url )
print (d.json())
