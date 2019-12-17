#!/usr/bin/env python3
"""upload derived data to scicat"""
import os
import urllib.parse
import platform
import socket
import json
import pwd

import getpass
import keyring
import requests


class SciCatManager:
    """fetch and delete from scicat"""
    username = "anonymoususer"
    name = "Anonymous User"
    email = "anonymous.user@mail.fjref.dk"

    def __init__(self):
        self.get_details()

    def fetch_login_from_keyring(self):
        """"fetch login from keyring"""
        if platform.system() == 'Darwin':
            print('darwin')
            username = "brightness"
            username = "ingestor"
            #username = self.username
            password = keyring.get_password('scicat', username)
            if not password:
                print("No password found in keychain, please enter it now to store it.")
                password = getpass.getpass()
                keyring.set_password('scicat', username, password)

            config = {"username": username, "password": password}
            print(config["username"])
            print(config["password"])

        return config

    def get_details(self):
        """get user details"""
        self.username = getpass.getuser()
        self.name = pwd.getpwuid(os.getuid())[4]
        self.email = self.name.replace(" ", ".")+"@esss.se"
        self.hostname = socket.gethostname()

    def upload(self):
        """fetch"""
        base_url = "https://scicatapi.esss.dk/"
        if self.hostname == "CI0020036":
            base_url = "http://localhost:3000/"
        api_url = base_url + "api/v3/"
        user_url = base_url + "auth/msad"
        ingestor_url = api_url+"Users/login"
        login_url = user_url
        if self.hostname == "CI0020036":
            login_url = ingestor_url

        if platform.system() == 'Darwin':
            config = self.fetch_login_from_keyring()
        else:
            password = getpass.getpass()
            config = {"username": self.username, "password": password}
        #config = self.fetch_login_from_keyring()

        login = requests.post(login_url, data=config)

        login_response = login.json()
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
        response_dataset = requests.get(dataset_url)
        print(response_dataset.json())
        # exit()
        # mantid stuff

        prefix = "20.500.12269"
        pid = "x12134"

        derived_dataset = {
            "investigator": self.name,
            "inputDatasets": [
                "20.500.12269/BRIGHTNESS/V200198"
            ],
            "usedSoftware": [
                "Mantid"
            ],
            "jobParameters": {"cpus": "1"},
            "jobLogData": "string1",
            "pid": pid,
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

        delete_url = api_url + "Datasets/" + \
            urllib.parse.quote_plus(prefix+"/"+pid) + "?access_token="+token
        print(delete_url)
        delete_response = requests.delete(delete_url)
        print(delete_response.json())
        dataset_post = api_url + "DerivedDatasets?access_token="+token
        response = requests.post(dataset_post, json=derived_dataset)
        post_response = response.json()
        if "pid" in post_response:
            print(post_response["pid"])

        delete_orig_url = api_url + "Datasets/" + \
            urllib.parse.quote_plus(prefix+"/"+pid) + \
            "/origdatablocks?access_token="+token
        print(delete_orig_url)
        requests.delete(delete_orig_url)
        orig = {
            "size": 0,
            "dataFileList": [
                {
                    "path": "string",
                    "size": 0,
                    "time": "2019-06-28T10:14:10.425Z",
                    "chk": "string",
                    "uid": "string",
                    "gid": "string",
                    "perm": "string"
                }
            ],
            "ownerGroup": "ess",
            "accessGroups": [
                "loki",
                "odin"
            ],
            "datasetId": prefix+"/"+pid,
            "createdAt": "2019-06-28T10:14:10.425Z",
            "updatedAt": "2019-06-28T10:14:10.425Z"
        }

        orig_post = api_url + "OrigDatablocks?access_token="+token
        orig_response = requests.post(orig_post, json=orig)
        print(orig_response.json())

def main():
    """main"""
    sci = SciCatManager()
    sci.upload()

if __name__ == "__main__":
    main()
