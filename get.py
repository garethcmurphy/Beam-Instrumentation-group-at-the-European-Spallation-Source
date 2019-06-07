#!/usr/bin/env python3
import requests
import json
import os
import pwd
import getpass
import keyring
import urllib.parse
import platform


class SciCatManager:
    username = "anonymoususer"
    name = "Anonymous User"
    email = "anonymous.user@mail.fjref.dk"

    def __init__(self):
        self.get_details()

    def fetch_login_from_keyring(self):
        if platform.system() == 'Darwin':
            print('darwin')
            username="ingestor"
            username=self.username
            password=keyring.get_password('scicat', username)
            config = {"username": username, "password":password}
            print(config)

        return config





    def get_details(self):
        self.username = getpass.getuser()
        self.name = pwd.getpwuid(os.getuid())[4]
        self.email = self.name.replace(" ", ".")+"@esss.se"

    def fetch(self):
        base_url = "https://scicatapi.esss.dk/"
        base_url = "http://localhost:3000/"
        user_url = base_url + "auth/msad"
        api_url = base_url + "api/v3/"
        ingestor_url = api_url+"Users/login"
        login_url = user_url

        password = getpass.getpass()
        config={"username":self.username, "password":password}
        #config = self.fetch_login_from_keyring()
        
        r = requests.post(login_url, data=config)

        login_response = r.json()
        print(login_response)
        if "id" in login_response:
            token = login_response["id"]
        elif "access_token" in login_response:
            token = login_response["access_token"]
        else:
            print("Login failed - exiting")
            exit()

        # token = (login_response["id"])
        #pid = "20.500.12269%2FBRIGHTNESS%2FBeamInstrumentation0001"

        #dataset_url = api_url + "Datasets/"+pid+"?access_token="+token
        fields = {'text': 'nicos_00000187'}
        limit = {'limit': '1', 'order': "creationTime:desc"}
        fields_json = json.dumps(fields)
        limit_json = json.dumps(limit)
        fields_encode = urllib.parse.quote(fields_json)
        limit_encode = urllib.parse.quote(limit_json)
        dataset_url = api_url + "Datasets/fullquery?fields=" + \
            fields_encode+"&limits="+limit_encode+"&access_token="+token
        print(dataset_url)
        d = requests.get(dataset_url)
        print(d.json())
        #exit()
        # mantid stuff


        derived_dataset = {
            "investigator": self.name,
            "inputDatasets": [
                "20.500.12269/BRIGHTNESS/V200198"
            ],
            "usedSoftware": [
                "Mantid"
            ],
            "jobParameters": {"cpus":"1"},
            "jobLogData": "string1",
            "pid": "20.500.12269/x12134",
            "owner": self.name,
            "ownerEmail": self.email,
            "orcidOfOwner": "https://orcid.org/0000-0002-1825-0097",
            "contactEmail": self.email,
            "sourceFolder": "/users/detector/experiments/v20/default",
            "size": 0,
            "packedSize": 0,
            "creationTime": "2019-06-04T10:53:02.681Z",
            "keywords": [
                "neutron",
                "ess"
            ],
            "description": "Data from beamline at V20, HZB, postprocessed with Mantid",
            "datasetName": "V20 Postprocessed Mantid data",
            "classification": "new",
            "license": "CC-BY-4.0",
            "version": "1.01",
            "isPublished": False,
            "type": "derived",
            "ownerGroup": "ess",
            "accessGroups": [
                "loki",
                "odin"
            ],
            "updatedBy": "string14",
            "scientificMetadata": {
                "chopper_1_speed": {"u": "Hz", "v": "14"},
                "chopper_2_speed": {"u": "Hz", "v": "15"}
            }
        }

        dataset_post = api_url + "Datasets?access_token="+token
        r = requests.put(dataset_post, json=derived_dataset)
        print(r.json())


if __name__ == "__main__":
    scicatman = SciCatManager()
    scicatman.fetch()
