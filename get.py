#!/usr/bin/env python3
import requests
import json
import os
import pwd
import getpass


class SciCatManager:
    username = ""
    name = ""
    email = ""

    def __init__(self):
        self.get_details()

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
                "20.500.12269/BRIGHTNESS/V200198"
            ],
            "usedSoftware": [
                "Mantid"
            ],
            "jobParameters": {},
            "jobLogData": "string1",
            "pid": "x12134",
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
            "ownerGroup": "ess",
            "accessGroups": [
                "loki",
                "odin"
            ],
            "updatedBy": "string14",
            "scientificMetadata": {
                "chopper_1_speed": {"u": "Hz", "v": "14"}
            }
        }

        dataset_post = api_url + "DerivedDatasets?access_token="+token
        r = requests.put(dataset_post, json=derived_dataset)


if __name__ == "__main__":
    scicatman = SciCatManager()
    scicatman.fetch()
