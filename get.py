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
import scicat


class SciCatManager:
    """fetch and delete from scicat"""
    username = "anonymoususer"
    name = "Anonymous User"
    email = "anonymous.user@mail.fjref.dk"

    def __init__(self):
        scicat.login()
        self.userinfo = scicat.userinfo()
        print(self.userinfo)
        self.email = self.userinfo["currentUserEmail"]
        self.name = self.userinfo["currentUser"]



    def upload(self):
        """fetch"""
        scicat.upload("dataset name")

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


def main():
    """main"""
    sci = SciCatManager()
    sci.upload()

if __name__ == "__main__":
    main()
