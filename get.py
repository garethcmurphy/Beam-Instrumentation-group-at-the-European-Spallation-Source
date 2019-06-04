#!/usr/bin/env python3
import requests
import json
import os
import pwd
import getpass


class SciCatManager:
    username = ""
    name = ""
    def __init__(self):
        self.get_details()

    def get_details(self):
        self.username = getpass.getuser()
        self.name = pwd.getpwuid(os.getuid())[4]

    def fetch(self):
        base_url = "https://scicatapi.esss.dk/"
        base_url = "http://localhost:3000/"
        user_url = base_url + "auth/msad"
        api_url = base_url + "api/v3/"
        ingestor_url = api_url+"Users/login"
        login_url = ingestor_url

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
        print(login_response)
        token = (login_response["id"])
        pid = "20.500.12269%2FBRIGHTNESS%2FBeamInstrumentation0001"

        dataset_url = api_url + "Datasets/"+pid+"?access_token="+token
        d = requests.get(dataset_url)
        print(d.json())

        derived_dataset = {
            "investigator": self.name,
            "inputDatasets": [
                "20.500.12269/BRIGHTNESS/V200198",
                "20.500.12269/BRIGHTNESS/V200197",
            ],
            "usedSoftware": [
                "Mantid",
                "MantidPython"
            ],
            "jobParameters": {},
            "jobLogData": "string1",
            "scientificMetadata": {},
            "pid": "x12134",
            "owner": self.username,
            "ownerEmail": "string2",
            "orcidOfOwner": "string3",
            "contactEmail": "string4",
            "sourceFolder": "string5",
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
            "ownerGroup": "ess",
            "accessGroups": [
                "loki",
                "odin"
            ],
            "createdBy": "string13",
            "updatedBy": "string14",
            "createdAt": "2019-06-04T10:53:02.681Z",
            "updatedAt": "2019-06-04T10:53:02.681Z"
        }

        dataset_post = api_url + "DerivedDatasets?access_token="+token
        r = requests.put(dataset_post, data = derived_dataset)


if __name__ == "__main__":
    scicatman = SciCatManager()
    scicatman.fetch()
